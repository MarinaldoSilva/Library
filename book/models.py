from uuid import uuid4

from django.db import models


class Book(models.Model):

    STATUS_TYPES = (
        ("AVAILABLE", "Available"),
        ("BORROWED", "Borrowed"),
        ("RESERVED", "Reserved"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    subtitle = models.CharField(max_length=250, null=False, blank=False)
    author = models.ForeignKey("author.Author", on_delete=models.SET_NULL, name="author", blank=True, null=True)
    book_description = models.TextField()
    category = models.CharField(max_length=50, null=False, blank=False)
    publisher = models.CharField(max_length=150)
    publication_date = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    last_edition = models.DateField()
    ISBN = models.CharField(max_length=20, unique=True, help_text="20 caracteres")
    page_count = models.IntegerField()
    language = models.CharField(max_length=20)
    cover_url = models.URLField(max_length=300, blank=True, null=True, verbose_name="link da capa")
    status = models.CharField(choices=STATUS_TYPES, default="AVAILABLE")
    estoque = models.PositiveIntegerField(blank=True)
