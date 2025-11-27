"""Mapeamento das rotas específicas do app operacional (login/movimentação/relatório)."""

from django.urls import path

from . import views

app_name = "controle"

urlpatterns = [
    # Autenticação
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.LogoutPageView.as_view(), name="logout"),
    # Operações de estoque
    path("movimentacao/", views.movimentacao_simples, name="movimentacao"),
    path("relatorio/", views.relatorio_basico, name="relatorio"),
]
