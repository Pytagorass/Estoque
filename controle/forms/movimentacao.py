from django import forms

from ..models import Movimentacao


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
