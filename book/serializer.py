from rest_framework import serializers

from author.models import Author

from .models import Book

 
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):

    author_data = AuthorSerializer(source="author", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

        read_only_fields = ("id",)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
