from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo_estoque", "estoque_atual", "estoque_minimo", "ativo")
    search_fields = ("nome", "codigo_estoque")
    list_filter = ("ativo", "unidade")

# Register your models here.
