from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BorrowingViewSet

router = DefaultRouter()

router.register(r'books/', BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path('', include(router.urls))
]