from rest_framework import generics, serializers
from .models import Book
from author.models import Author
from .serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated


class BookListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Book.objects.all()
        return Book.objects.filter(author__user=user)
    
    def perform_create(self, serializer):   
        print(self.request)
        try:
            instance_author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            raise serializers.ValidationError({"error":"Autor não encontrado."})


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)
    