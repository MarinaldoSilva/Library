from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from user.serializer import UserSerializer

User = get_user_model()


class SingupAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Registrar novo usuário",
        description="Cria uma nova conta de usuário no sistema.",
        request=UserSerializer,
        responses={201: inline_serializer(
            name='SignupResponse',
            fields={
                'Info': serializers.CharField()
            }
        )}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"Info": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED
        )


class SingInAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login de usuário",
        description="Autentica um usuário com email e senha e retorna os tokens JWT.",
        request=inline_serializer(
            name='LoginRequest',
            fields={
                'email': serializers.EmailField(),
                'password': serializers.CharField(write_only=True)
            }
        ),
        responses={201: inline_serializer(
            name='LoginResponse',
            fields={
                'id': serializers.IntegerField(),
                'username': serializers.CharField(),
                'email': serializers.EmailField(),
                'access': serializers.CharField(),
                'refresh': serializers.CharField(),
            }
        )}
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuário não cadastrado."}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            refresh_token = TokenObtainPairSerializer.get_token(user)
            token_access = refresh_token.access_token

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access": str(token_access),
                    "refresh": str(refresh_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Verifique email e senha e tente novamente."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class SingOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout de usuário",
        description="Invalida o Refresh Token, realizando o logout.",
        request=inline_serializer(
            name='LogoutRequest',
            fields={
                'refresh': serializers.CharField()
            }
        ),
        responses={204: None}
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"Error": "O token não foi informado"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed(
                {"Error": "Não foi possível invalidar o token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)