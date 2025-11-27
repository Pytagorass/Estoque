from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from catalogo.models import Item


class Movimentacao(models.Model):
    """Histórico simples de entradas e saídas de um item."""

    TIPOS = [
        ("ENTRADA", "Entrada"),
        ("SAIDA", "Saída"),
    ]

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=8, choices=TIPOS, default="ENTRADA")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    data = models.DateField(default=timezone.now)
    responsavel = models.CharField(max_length=80)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ("-data", "-id")

    def _delta(self):
        """Retorna o valor que será aplicado ao estoque (positivo ou negativo)."""
        return self.quantidade if self.tipo == "ENTRADA" else -self.quantidade

    def clean(self):
        """Previne saídas com estoque negativo e garante quantidade positiva."""
        if self.quantidade <= 0:
            raise ValidationError({"quantidade": "Informe uma quantidade positiva."})
        if self.tipo == "SAIDA":
            estoque_disponivel = self.item.estoque_atual
            if self.pk:
                original = Movimentacao.objects.get(pk=self.pk)
                if original.item_id == self.item_id and original.tipo == "SAIDA":
                    estoque_disponivel += original.quantidade
            if estoque_disponivel < self.quantidade:
                raise ValidationError(
                    {"quantidade": f"Saída maior que o estoque disponível ({estoque_disponivel})."}
                )

    def save(self, *args, **kwargs):
        """Aplica o delta na tabela de Item sempre que a movimentação é gravada."""
        is_new = self._state.adding
        original_delta = Decimal("0")
        if not is_new:
            original = Movimentacao.objects.get(pk=self.pk)
            original_delta = original._delta()
        self.full_clean()
        super().save(*args, **kwargs)
        delta = self._delta() - original_delta
        item = self.item
        item.estoque_atual = max(Decimal("0"), item.estoque_atual + delta)
        item.save(update_fields=["estoque_atual"])

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.item.nome}"
