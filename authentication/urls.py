from .views import SingupAPIView, SingInAPIView, SingOutAPIView
from django.urls import path, URLPattern


urlpatterns:URLPattern = [
    path("register/", SingupAPIView.as_view(), name="register"),
    path("login/", SingInAPIView.as_view(), name="login"),
    path("logout/", SingOutAPIView.as_view(), name="logout")
]