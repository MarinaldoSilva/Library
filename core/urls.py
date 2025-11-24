from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/library/", include("book.urls")),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/borrowing/", include("borrowing.urls")),
    path("api/v1/authors/", include("author.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
