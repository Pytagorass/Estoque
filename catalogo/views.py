from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.deletion import ProtectedError

from .forms import ItemForm
from .models import Item


@login_required
def cadastro_itens(request):
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
            return redirect("catalogo:cadastro_itens")
    else:
        form = ItemForm()
    return render(
        request,
        "catalogo/cadastro_itens.html",
        {"form": form, "itens": itens, "stats": stats},
    )


@login_required
def editar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"{item.nome} atualizado com sucesso.")
            return redirect("catalogo:cadastro_itens")
    else:
        form = ItemForm(instance=item)
    return render(request, "catalogo/item_form.html", {"form": form, "item": item})


@login_required
def excluir_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        nome = item.nome
        try:
            item.delete()
            messages.success(request, f"Item {nome} removido.")
        except ProtectedError:
            messages.error(
                request,
                "Não é possível excluir este item porque existem movimentações associadas. "
                "Remova ou ajuste as movimentações antes de excluir.",
            )
        return redirect("catalogo:cadastro_itens")
    return render(request, "catalogo/item_confirm_delete.html", {"item": item})

# Create your views here.
