from django.urls import path
from app import views

urlpatterns = [
    # Rotas de endereço
    path('enderecos/criar/',views.CriarEnderecoView.as_view(), name='criar_endereco'),
]