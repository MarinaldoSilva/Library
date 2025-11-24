from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import UserSerializer

User = get_user_model()


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Visualizar meu perfil", description="Retorna os dados do perfil do usuário logado.", responses={200: UserSerializer})
    def get(self, request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Atualizar meu perfil", description="Atualiza parcialmente os dados do usuário logado.", request=UserSerializer, responses={200: UserSerializer})
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(summary="Deletar usuário", description="Exclui um usuário específico pelo ID. Apenas para administradores.", responses={204: None})
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
