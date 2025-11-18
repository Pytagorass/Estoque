from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Item(models.Model):
    UNIDADES = [
        ("UN", "Unidade"),
        ("KG", "Quilo"),
        ("L", "Litro"),
    ]

    nome = models.CharField(max_length=120)
    codigo_estoque = models.CharField("Código de estoque", max_length=30, unique=True)
    unidade = models.CharField(max_length=2, choices=UNIDADES, default="UN")
    estoque_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    estoque_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
    )
    observacao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("nome",)

    def clean(self):
        if not self.nome:
            raise ValidationError({"nome": "Informe o nome do item."})
        if not self.codigo_estoque:
            raise ValidationError({"codigo_estoque": "Informe o código de estoque."})
        if self.estoque_atual < 0:
            raise ValidationError({"estoque_atual": "O estoque não pode ser negativo."})
        if self.estoque_minimo < 0:
            raise ValidationError({"estoque_minimo": "O estoque mínimo precisa ser positivo."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def em_alerta(self):
        return self.estoque_atual <= self.estoque_minimo

    def __str__(self):
        return f"{self.nome} ({self.codigo_estoque})"


class Movimentacao(models.Model):
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
        return self.quantidade if self.tipo == "ENTRADA" else -self.quantidade

    def clean(self):
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
