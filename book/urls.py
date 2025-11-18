from django.urls import path, URLPattern
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView


urlpatterns:URLPattern = [
    path("books/", BookListCreateAPIView.as_view(), name="books_list_create"),
    path("books/<pk>/", BookRetrieveUpdateDestroyAPIView.as_view(), name="books_detail")
]