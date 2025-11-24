from django.urls import URLPattern, path

from .views import (
    BookChangeStatusAPIView,
    BookCreateAPIView,
    BookDeleteAPIView,
    BookDetailAPIView,
    BookListAPIView,
    BookUpdateAPIView,
)

urlpatterns:URLPattern = [
    path("books/", BookListAPIView.as_view(), name="book-list"),
    path("books/create/", BookCreateAPIView.as_view(), name="book-create"),
    path("books/<uuid:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
    path("books/<uuid:pk>/update/", BookUpdateAPIView.as_view(), name="book-update"),
    path("books/<uuid:pk>/status/", BookChangeStatusAPIView.as_view(), name="book-status"),
    path("books/<uuid:pk>/delete/", BookDeleteAPIView.as_view(), name="book-delete"),
]