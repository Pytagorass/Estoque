from django.urls import path

from . import views

app_name = "controle"

urlpatterns = [
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.LogoutPageView.as_view(), name="logout"),
    path("itens/", views.cadastro_itens, name="cadastro_itens"),
    path("itens/<int:pk>/editar/", views.editar_item, name="editar_item"),
    path("itens/<int:pk>/excluir/", views.excluir_item, name="excluir_item"),
    path("movimentacao/", views.movimentacao_simples, name="movimentacao"),
    path("relatorio/", views.relatorio_basico, name="relatorio"),
]
