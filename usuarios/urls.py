from django.urls import path
from usuarios import views

urlpatterns = [
    # Rotas de usuário
    path('usuarios/criar/', views.CriarUsuarioView.as_view(), name='criar_usuario'),  # POST
]