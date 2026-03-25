from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers.enderecosSerializers import CriarEnderecoSerializer, EnderecoResponseSerializer, ListarEnderecoEspecificoSerializer
from app.services.enderecosServices import criar_endereco_service, listar_endereco_especifico_service

class CriarEnderecoView(APIView):

    @staticmethod
    def post(request):
        try:
            serializer = CriarEnderecoSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": "Erro ao salvar endereço",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            endereco = criar_endereco_service(serializer.validated_data)
            endereco_serializer = EnderecoResponseSerializer(endereco)

            return Response({
                "sucess": True,
                "message": "Endereço criado com sucesso",
                "endereco": endereco_serializer.data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Um erro inesperado ocorreu",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListarEnderecoEspecificoView(APIView):

    @staticmethod
    def get(request, pk):
        try:
            endereco = listar_endereco_especifico_service(pk)

            if not endereco:
                return Response({
                    "success": False,
                    "message": "Endereço não encontrado"
                }, status=status.HTTP_404_NOT_FOUND)

            endereco_serializer = ListarEnderecoEspecificoSerializer(endereco)

            return Response({
                "success": True,
                "message": "Endereço encontrado com sucesso",
                "endereco": endereco_serializer.data,
            })

        except Exception as e:
            return Response({
                "success": False,
                "message": "Um erro inesperado ocorreu",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
