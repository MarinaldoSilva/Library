from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from author.models import Author
from author.serializer import AuthorSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar Autores (Com Filtro de Visibilidade)",
        description="""
        Retorna uma lista de autores. 
        
        **Lógica de Visibilidade:**
        * **Superusuários/Staff:** Veem TODOS os autores do sistema.
        * **Usuários Comuns:** Veem apenas os autores que ELES MESMOS cadastraram.
        """,
    ),
    create=extend_schema(summary="Cadastrar novo Autor", description="Cria um novo registro de autor vinculado ao usuário logado."),
    retrieve=extend_schema(summary="Detalhes de um Autor"),
    update=extend_schema(summary="Atualizar Autor"),
    destroy=extend_schema(summary="Excluir Autor"),
)
class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]

    filter_fields = ["name"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Author.objects.all()
        return Author.objects.filter(user=user)
