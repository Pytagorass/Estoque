from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Item, Movimentacao


class ItemForm(forms.ModelForm):
    """Formulário principal para criação/edição de itens do catálogo."""

    class Meta:
        model = Item
        fields = ["nome", "codigo_estoque", "unidade", "estoque_minimo", "observacao", "ativo"]

    def clean_nome(self):
        return self.cleaned_data["nome"].strip()

    def clean_codigo_estoque(self):
        return self.cleaned_data["codigo_estoque"].strip().upper()


class MovimentacaoForm(forms.ModelForm):
    """Utilizado nas entradas/saídas rápidas exibidas no painel."""

    class Meta:
        model = Movimentacao
        fields = ["item", "tipo", "quantidade", "data", "responsavel", "observacao"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_responsavel(self):
        return self.cleaned_data["responsavel"].strip()


class LoginForm(AuthenticationForm):
    """Formulário baseado no AuthenticationForm padrão, com labels em português."""

    username = forms.CharField(label="Usuário", max_length=150, widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
