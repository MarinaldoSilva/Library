from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","birth_date","username","password","first_name","last_name","full_name", "created_at", "updated_at", "status")
        read_only_fields = ("id", "created_at", "updated_at")#apenas visualização

        extra_kwargs = {
            'password': {
                'write_only':True,
            }
        }

    def create(self, validated_data)->User:
        new_user = User.objects.create_user(**validated_data)
        return new_user

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