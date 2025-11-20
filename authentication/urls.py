from django.urls import URLPattern, path

from .views import SingInAPIView, SingOutAPIView, SingupAPIView

urlpatterns: URLPattern = [
    path("register/", SingupAPIView.as_view(), name="register"),
    path("login/", SingInAPIView.as_view(), name="login"),
    path("logout/", SingOutAPIView.as_view(), name="logout"),
]
