from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "Usuário"
        MANAGER = "MANAGER", "Gestor"
        ADMIN = "ADMIN", "Administrador"

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=9, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    suspended_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    def __str__(self):
        return self.email
