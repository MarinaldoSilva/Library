from rest_framework import serializers
from .models import Book
from author.models import Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    
    author_data = AuthorSerializer(source='author',read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

        read_only_fields = ("id",)

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)