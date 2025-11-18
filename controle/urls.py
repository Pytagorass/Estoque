from django.urls import path

from . import views

app_name = "controle"

urlpatterns = [
    path("itens/", views.cadastro_itens, name="cadastro_itens"),
    path("itens/<int:pk>/editar/", views.editar_item, name="editar_item"),
    path("itens/<int:pk>/excluir/", views.excluir_item, name="excluir_item"),
    path("movimentacao/", views.movimentacao_simples, name="movimentacao"),
    path("relatorio/", views.relatorio_basico, name="relatorio"),
]
