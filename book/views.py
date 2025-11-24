from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from drf_spectacular.utils import extend_schema

from .serializer import Borrowing, BorrowingSerializer


class BorrowingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar Empréstimos",
        description="Lista os empréstimos. Admins veem todos, usuários veem apenas os seus.",
        responses={200: BorrowingSerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        if user.is_staff or user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=user)
        serializer = BorrowingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowingCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Realizar Empréstimo",
        description="Registra um novo empréstimo e atualiza o status do livro para BORROWED.",
        request=BorrowingSerializer,
        responses={201: BorrowingSerializer}
    )
    def post(self, request):
        serializer = BorrowingSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        borrowing_instance = serializer.save(user=request.user)
        
        book_instance = borrowing_instance.book
        book_instance.status = 'BORROWED'
        book_instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Detalhar Empréstimo",
        description="Retorna detalhes de um empréstimo específico.",
        responses={200: BorrowingSerializer}
    )
    def get(self, request, pk):
        
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                queryset = Borrowing.objects.get(pk=pk)
            else:
                queryset = Borrowing.objects.get(pk=pk, user=user)
        except Borrowing.DoesNotExist:
            raise NotFound("Emprestimo Não localizado ou você nao tem acesso a essa opção.")
        
        serializer = BorrowingSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowingUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Atualizar Empréstimo",
        description="Atualiza dados de um empréstimo existente.",
        request=BorrowingSerializer,
        responses={200: BorrowingSerializer}
    )
    def patch(self, request, pk):
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                queryset = Borrowing.objects.get(pk=pk)
            else:
                queryset = Borrowing.objects.get(pk=pk, user=user)
        except Borrowing.DoesNotExist:
            raise NotFound("Não é possível atualizar o emprestimo")
        serializer = BorrowingSerializer(instance=queryset, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowingRenewalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Renovar Empréstimo",
        description="Estende a data de devolução em 7 dias, caso o livro não esteja reservado.",
        request=None,
        responses={200: BorrowingSerializer}
    )
    def patch(self, request, pk):
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                borrowing = Borrowing.objects.get(pk=pk)
            else:
                borrowing = Borrowing.objects.get(pk=pk, user=user)
        except Borrowing.DoesNotExist:
            raise NotFound("Borrowing not found.")   
        
        book = borrowing.book
        if book.status == 'RESERVED':
            return Response({"error":"Cannot renew. This book is reserved by another user."}, status=status.HTTP_400_BAD_REQUEST)
        borrowing.return_date += timedelta(days=7)
        borrowing.save()
        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowingDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Devolver/Excluir Empréstimo",
        description="Remove o empréstimo e atualiza o status do livro para AVAILABLE.",
        responses={204: None}
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                queryset = Borrowing.objects.get(pk=pk)
            else:
                queryset = Borrowing.objects.get(pk=pk, user=user)
        except Borrowing.DoesNotExist:
            raise NotFound("Não é possível atualizar o emprestimo")

        book = queryset.book
        book.status = 'AVAILABLE'
        book.save()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)