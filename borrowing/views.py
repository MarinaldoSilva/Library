from datetime import timedelta

from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiTypes

from .models import Borrowing
from .service import service_create
from .serializer import BorrowingSerializer


class BorrowingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Listar Empréstimos", description="Retorna a lista de empréstimos. Superusuários veem tudo; usuários comuns veem apenas os seus.", responses={200: BorrowingSerializer(many=True)})
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
            summary="Criar Empréstimo", description="Cria um novo registro de empréstimo e muda o status do livro para 'BORROWED'.", request=BorrowingSerializer, responses={201: BorrowingSerializer})
    def post(self, request):
        serializer = BorrowingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']
        return_date = serializer.validated_data['return_date']
        user = request.user

        try:
            borrowing = service_create(
                user=user,
                book=book,
                return_date=return_date
            )
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_borrowing = BorrowingSerializer(borrowing)
        return Response(serializer_borrowing.data, status=status.HTTP_201_CREATED)


class BorrowingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhes do Empréstimo", description="Busca um empréstimo específico pelo ID.", responses={200: BorrowingSerializer, 404: OpenApiTypes.OBJECT})
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

    @extend_schema(summary="Atualizar Empréstimo (Parcial)", description="Atualiza campos específicos de um empréstimo.", request=BorrowingSerializer, responses={200: BorrowingSerializer})
    def patch(self, request, pk):
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                queryset = Borrowing.objects.get(pk=pk)
            else:
                queryset = Borrowing.objects.get(pk=pk, user=user)
        except Borrowing.DoesNotExist:
            raise NotFound("Não é possível atualizar o emprestimo")
        serializer = BorrowingSerializer(instance=queryset, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowingRenewalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Renovar Empréstimo (+7 Dias)", description="Adiciona 7 dias à data de devolução, se o livro não estiver reservado.", request=None, responses={200: BorrowingSerializer, 400: OpenApiTypes.OBJECT})
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
        if book.status == "RESERVED":
            return Response({"error": "Não é possível reservar um livro já reservado por outro usuário."}, status=status.HTTP_400_BAD_REQUEST)
        borrowing.return_date += timedelta(days=7)
        borrowing.save()
        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowingDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Excluir Empréstimo", description="Remove o registro de empréstimo e libera o livro (status AVAILABLE).", responses={204: None})
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
        book.status = "AVAILABLE"
        book.save()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
