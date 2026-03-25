from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers.enderecosSerializers import CriarEnderecoSerializer, EnderecoResponseSerializer
from app.services.enderecosServices import criar_endereco_service

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
