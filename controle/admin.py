from django.contrib import admin

from .models import Movimentacao


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "item", "quantidade", "data", "responsavel")
    list_filter = ("tipo", "data")
    search_fields = ("item__nome", "responsavel")
