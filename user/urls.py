from django.urls import path

from .views import MyProfileAPIView, UpdateProfileAPIView, UserDeleteAPIView

urlpatterns = [
    path("editar/", UpdateProfileAPIView.as_view(), name="user_update"),
    path("perfil/", MyProfileAPIView.as_view(), name="user_profile"),
    path("users/<int:pk>/", UserDeleteAPIView.as_view(), name="user-delete"),
]
