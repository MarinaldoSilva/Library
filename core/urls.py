from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/',include('user.urls')),
    path('api/v1/library/', include('book.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/borrowing/', include('borrowing.urls')),
    path('api/v1/authors/', include('author.urls'))
]
