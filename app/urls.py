from django.urls import path
from app import views

urlpatterns = [
    # Rotas de endereço
    path('enderecos/criar/', views.CriarEnderecoView.as_view(), name='criar_endereco'),
    path('enderecos/listagem_especifica/<int:pk>/', views.ListarEnderecoEspecificoView.as_view(), name='listar_endereco_especifico'),
]
