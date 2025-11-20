from rest_framework import viewsets, serializers
from author.serializer import AuthorSerializer
from author.models import Author
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]

    filter_fields = ["name"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Author.objects.all()
        return Author.objects.filter(user=user)
