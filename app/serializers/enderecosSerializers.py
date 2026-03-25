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

class EnderecoResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = '__all__'