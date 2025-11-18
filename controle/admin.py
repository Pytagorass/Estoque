from django.contrib import admin

from .models import Item, Movimentacao


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo_estoque", "unidade", "estoque_atual", "estoque_minimo", "ativo")
    search_fields = ("nome", "codigo_estoque")
    list_filter = ("ativo",)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "item", "quantidade", "data", "responsavel")
    list_filter = ("tipo", "data")
    search_fields = ("item__nome", "responsavel")
