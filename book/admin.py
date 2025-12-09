from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "last_edition")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "ISBN", "author__name")
    ordering = ("title",)
    