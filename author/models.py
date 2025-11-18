from django.db import models
from uuid import uuid4

class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    biography = models.TextField()
    birth_date = models.DateField()
    nationality = models.CharField(max_length=20)
