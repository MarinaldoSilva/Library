from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "birth_date",
            "username",
            "password",
            "first_name",
            "last_name",
            "full_name",
            "created_at",
            "updated_at",
            "status",
        )
        read_only_fields = ("id", "created_at", "updated_at")  # apenas visualização

        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    """Cria um usuário com os dados que request.data, a função create_user recebe esse dict e com o ** é desempacotado e cria o usuário com esses dados, além disso o metodo já faz o hash da senha a mantendo criptografada."""

    def create(self, validated_data) -> User:
        new_user = User.objects.create_user(**validated_data)
        return new_user

    """O método não faz o hash da senha, então removemos do dict, fazemos o hash com o set_password(password) e pegamos o instance.campo_db e pegamos o valor do dict com o get e adicionamos na váriavel, se não tiver esse valor no nosso dict, mantemos o valor que já vem no banco com o instance.campo_db e salvamos com o instance.save() e retornamos o instance novamente."""

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        return instance
