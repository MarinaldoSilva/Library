from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=False)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["birth_date", "full_name"]

    def __str__(self):
        return f"Usuário {self.username} criado com sucesso."
