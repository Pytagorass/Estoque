from django import forms

from produto.models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        # disponibilizando atributos da classe Produto
        model = Produto
        fields = ('categoria', 'produto_nome', 'descricao', 'preco', 'estoque', 'slug', 'esta_disponivel')
        # fields = '_all_' --> disponibilza todos os atributos do model (Produto)