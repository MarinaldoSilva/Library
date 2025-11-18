from rest_framework import generics
from .models import Book
from .serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated


class BookListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)

    def perform_create(self, serializer):   
        serializer.save(author = self.request.user)

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)
    