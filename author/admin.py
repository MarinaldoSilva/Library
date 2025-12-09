from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "nationality", "birth_date")
    list_filter = ("nationality","name")
    search_fields = ("name", "biography", "nationality")
    ordering = ("name",)