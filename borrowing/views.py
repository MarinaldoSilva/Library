from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializer import Borrowing, BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    filter
    serializer_class = BorrowingSerializer
    filter_backends = [DjangoFilterBackend]

    filter_fields = ["user", "book", "borrow_date", "return_date"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
