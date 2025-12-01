from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializer import BookSerializer, BookBulkSerializer


class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar Livros", description="Lista os livros. Admins veem todos; usuários também podem ver todos ou aplicar filtros no cliente.", responses={200: BookSerializer(many=True)})
    def get(self, request):

        #adicionado o select_related() paRa buscaR o autor e livro na mesma consulta complexa.
        queryset = Book.objects.select_related('author').all()

        category = request.query_params.get("category")
        author_name = request.query_params.get("auhtor")
        status_param = request.query_params.get("status")

        ordering = request.query_params.get("ordering")

        if category:
            queryset = queryset.filter(category__icontains=category)

        if author_name:
            queryset = queryset.filter(author_name__icontains=author_name)

        if status_param:
            queryset = queryset.filter(status_param__icontains=status_param)

        search_validated = ["title", "publication_date", "author_name"]

        if ordering in search_validated:
            queryset = queryset.order_by(ordering)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookBulkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Importação em Massa de Livros",
        description="Cria múltiplos livros de uma vez.",
        request=BookBulkSerializer(many=True),
        responses={201: BookBulkSerializer(many=True)}
    )

    def post(self, request):
        serializer = BookBulkSerializer(data = request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class BookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Criar Livro", description="Cria um novo registro de livro.", request=BookSerializer, responses={201: BookSerializer})
    def post(self, request):
        serializer = BookSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhar Livro", description="Retorna detalhes de um livro específico.", responses={200: BookSerializer})
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound("Livro não localizado.")

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Atualizar Livro", description="Atualiza dados de um livro existente.", request=BookSerializer, responses={200: BookSerializer})
    def patch(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound("Livro não localizado na base de dados.")
        serializer = BookSerializer(instance=book, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookChangeStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Alterar status do Livro", description="Altera o campo `status` do livro (ex.: AVAILABLE, BORROWED, RESERVED).", request=None, responses={200: BookSerializer})
    def patch(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound("Livro não encontrado.")

        new_status = request.data.get("status")
        if not new_status:
            return Response({"error": "Status do livro não definido."}, status=status.HTTP_400_BAD_REQUEST)

        book.status = new_status
        book.save()
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Excluir Livro", description="Remove o registro do livro.", responses={204: None})
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound("Não é possível excluir o livro")

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
