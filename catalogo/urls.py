"""Rotas do app de catálogo de itens."""

from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.cadastro_itens, name="cadastro_itens"),
    path("<int:pk>/editar/", views.editar_item, name="editar_item"),
    path("<int:pk>/excluir/", views.excluir_item, name="excluir_item"),
]
