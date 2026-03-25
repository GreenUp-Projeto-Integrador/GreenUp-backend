from django.db import models

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=50)
