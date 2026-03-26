from rest_framework import serializers
from app.models.enderecosModel import Endereco

class CriarEnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = '__all__'

class ListarEnderecoEspecificoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = '__all__'

class UpdateEnderecoSerializer(serializers.ModelSerializer):
    cep = serializers.CharField(required=False)
    cidade = serializers.CharField(required=False)
    estado = serializers.CharField(required=False)
    rua = serializers.CharField(required=False)
    numero = serializers.CharField(required=False)
    complemento = serializers.CharField(required=False)

    def validate(self, attrs):
        campos_validos = set(self.fields.keys())
        campos_recebidos = set(self.initial_data.keys())
        campos_invalidos = campos_recebidos - campos_validos

        if campos_invalidos:
            raise serializers.ValidationError(f"Campos inválidos: {campos_invalidos}")

        return attrs

    class Meta:
        model = Endereco
        fields = '__all__'

class EnderecoResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = '__all__'
