from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ItemForm
from ..models import Item


@login_required
def cadastro_itens(request):
    """Exibe o catálogo e estatísticas básicas, além do formulário de criação."""
    itens_queryset = Item.objects.order_by("nome")
    itens = list(itens_queryset)
    stats = {
        "total": len(itens),
        "ativos": sum(1 for item in itens if item.ativo),
        "alertas": sum(1 for item in itens if item.em_alerta),
    }
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Item {item.nome} cadastrado.")
            return redirect("controle:cadastro_itens")
    else:
        form = ItemForm()
    return render(
        request,
        "controle/cadastro_itens.html",
        {
            "form": form,
            "itens": itens,
            "stats": stats,
        },
    )


@login_required
def editar_item(request, pk):
    """Permite alterar os dados de um item já cadastrado."""
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"{item.nome} atualizado com sucesso.")
            return redirect("controle:cadastro_itens")
    else:
        form = ItemForm(instance=item)
    return render(
        request,
        "controle/item_form.html",
        {
            "form": form,
            "item": item,
        },
    )


@login_required
def excluir_item(request, pk):
    """Fluxo de confirmação para remover um item do catálogo."""
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        nome = item.nome
        item.delete()
        messages.success(request, f"Item {nome} removido.")
        return redirect("controle:cadastro_itens")
    return render(
        request,
        "controle/item_confirm_delete.html",
        {"item": item},
    )
