from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "full_name","status")
    list_filter = ("status",)
    search_fields = ("username", "email", "full_name")
    ordering = ("username",)
    
admin.site.register(User, CustomUserAdmin)