from rest_framework import serializers
from usuarios.models.usuariosModel import Usuario

class CriarUsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'nome_completo', 'email', 'senha']
        read_only_fields = ['id']

class UsuarioResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nome_completo', 'email', 'status']
