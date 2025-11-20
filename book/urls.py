from django.urls import URLPattern, path

from .views import (
    BookListAPIView,
    BookCreateAPIView,
    BookDetailAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView
)


urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<uuid:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<uuid:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<uuid:pk>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),
]




























# urlpatterns: URLPattern = [
#     path("books/", BookListCreateAPIView.as_view(), name="books_list_create"),
#     path(
#         "books/<pk>/", BookRetrieveUpdateDestroyAPIView.as_view(), name="books_detail"
#     ),
# ]
