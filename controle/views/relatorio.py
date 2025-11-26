from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from ..models import Item, Movimentacao


@login_required
def relatorio_basico(request):
    """Relatório enxuto focado nos últimos 7 dias e nos itens em alerta."""
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
