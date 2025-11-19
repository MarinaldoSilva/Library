from django.db import models
from django.conf import settings
from uuid import uuid4

class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='author_profile',
        unique=True 
    )
    name = models.CharField(max_length=255)
    biography = models.TextField()
    birth_date = models.DateField()
    nationality = models.CharField(max_length=20)
