from usuarios.models.usuariosModel import Usuario
from django.contrib.auth.hashers import make_password

def criar_usuario_service(data):

    data = dict(data)
    data['senha_hash'] = make_password(data.pop('senha'))
    usuario = Usuario.objects.create(**data)
    return usuario
