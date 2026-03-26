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

def update_endereco_service(data, pk):
    try:
        endereco_obj = Endereco.objects.get(pk=pk)
    except Endereco.DoesNotExist:
        return None

    for key, value in data.items():
        setattr(endereco_obj, key, value)

    endereco_obj.save(update_fields=data.keys())
    return endereco_obj
