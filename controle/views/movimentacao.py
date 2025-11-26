from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import redirect, render

from ..forms import MovimentacaoForm
from ..models import Item, Movimentacao


@login_required
def movimentacao_simples(request):
    """Tela de lançamentos rápidos com painel de indicadores."""
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
