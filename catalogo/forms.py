
from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    """Formulário principal para criação/edição de itens do catálogo."""

    class Meta:
        model = Item
        fields = ["nome", "codigo_estoque", "unidade", "estoque_minimo", "observacao", "ativo"]

    def clean_nome(self):
        return self.cleaned_data["nome"].strip()

    def clean_codigo_estoque(self):
        return self.cleaned_data["codigo_estoque"].strip().upper()
