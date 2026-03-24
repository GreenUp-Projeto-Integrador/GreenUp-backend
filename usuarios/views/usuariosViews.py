from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.serializers.usuariosSerializers import CriarUsuarioSerializer, UsuarioResponseSerializer
from usuarios.services.usuariosServices import criar_usuario_service

class CriarUsuarioView(APIView):

    @staticmethod
    def post(request):
        try:
            serializer = CriarUsuarioSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            usuario = criar_usuario_service(serializer.validated_data)
            usuario_serializer = UsuarioResponseSerializer(usuario)

            return Response({
                "success": True,
                "message": "Usuário criado com sucesso.",
                "usuario": usuario_serializer.data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
