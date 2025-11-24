from uuid import uuid4

from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    name = models.CharField(max_length=255, unique=True)
    biography = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"
