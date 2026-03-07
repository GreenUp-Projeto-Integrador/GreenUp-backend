from django.db import models

class Status(models.TextChoices):
    ATIVO = "A", "Ativo"
    INATIVO = "IN", "Inativo"
    DELETADO = "DEL", "Deletado"
