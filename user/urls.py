from django.urls import path
from .views import MyProfileAPIView, UpdateProfileAPIView


urlpatterns = [
    path('editar/', UpdateProfileAPIView.as_view(), name='user_update'),
    path('perfil/', MyProfileAPIView.as_view(), name='user_profile')
]