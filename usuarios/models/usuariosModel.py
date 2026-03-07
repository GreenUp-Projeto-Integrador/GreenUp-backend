from django.db import models
from usuarios.enums.statusUsuario import Status

class Usuario(models.Model):

    username = models.CharField(max_length=50)
    nome_completo = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=255)
    status = models.CharField(choices=Status.choices, default=Status.ATIVO, null=True, blank=True)
    # tipo_usuario = ... Implementar quando existir a entidade TipoUsuario
