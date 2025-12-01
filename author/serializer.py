from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

        read_only_fields = ("id",)  # apenas visualização

        """write_only = recebe no POST, mas não é retornado no GET"""
        extra_kwargs = {"user": {"write_only": True, "required": False}}
