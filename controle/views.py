from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ItemForm, LoginForm, MovimentacaoForm
from .models import Item, Movimentacao


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


@login_required
def movimentacao_simples(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save()
            messages.success(request, f"{mov.get_tipo_display()} registrada para {mov.item.nome}.")
            return redirect("controle:movimentacao")
    else:
        form = MovimentacaoForm(initial={"responsavel": request.user.get_username() or ""})
    ultimas = Movimentacao.objects.select_related("item").order_by("-data", "-id")[:10]
    indicadores = {
        "saldo_total": Item.objects.aggregate(total=Sum("estoque_atual"))["total"] or 0,
        "alertas": Item.objects.filter(estoque_atual__lte=F("estoque_minimo")).count(),
        "itens_movimentados": Movimentacao.objects.values("item").distinct().count(),
    }
    return render(
        request,
        "controle/movimentacao.html",
        {
            "form": form,
            "movimentacoes": ultimas,
            "indicadores": indicadores,
        },
    )


@login_required
def relatorio_basico(request):
    itens = list(Item.objects.order_by("nome"))
    ultimos_dias = timezone.now().date() - timedelta(days=7)
    totais = (
        Movimentacao.objects.filter(data__gte=ultimos_dias)
        .values("tipo")
        .annotate(total=Sum("quantidade"))
    )
    resumo_periodo = {linha["tipo"]: linha["total"] or 0 for linha in totais}
    abaixo_minimo = [item for item in itens if item.em_alerta]
    return render(
        request,
        "controle/relatorio.html",
        {
            "itens": itens,
            "resumo_periodo": resumo_periodo,
            "abaixo_minimo": abaixo_minimo,
            "periodo_inicio": ultimos_dias,
            "total_itens": len(itens),
            "ativos": sum(1 for item in itens if item.ativo),
        },
    )


class LoginPageView(LoginView):
    template_name = "conta/login.html"
    form_class = LoginForm


class LogoutPageView(LogoutView):
    next_page = "controle:login"
