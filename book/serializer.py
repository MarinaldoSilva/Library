from rest_framework import serializers
from .models import Book
from author.serializer import AuthorSerializer as AuthorNameIdSerializer


class BookSerializer(serializers.ModelSerializer):
    
    author = AuthorNameIdSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

        read_only_fields = ("id",)

    def create(self, validated_data):
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)