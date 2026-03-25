from app.models.enderecosModel import Endereco

def criar_endereco_service(data):
    endereco = Endereco.objects.create(**data)
    return endereco
