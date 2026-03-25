from app.models.enderecosModel import Endereco

def criar_endereco_service(data):
    endereco = Endereco.objects.create(**data)
    return endereco

def listar_endereco_especifico_service(pk):
    try:
        endereco = Endereco.objects.get(pk=pk)
        return endereco
    except Endereco.DoesNotExist:
        return None
