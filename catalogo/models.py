from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    """Representa um insumo controlado pelo barco-hotel."""

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
        app_label = "controle"

    def clean(self):
        """Regra de negócio: nenhum estoque negativo ou código em branco."""
        if not self.nome:
            raise ValidationError({"nome": "Informe o nome do item."})
        if not self.codigo_estoque:
            raise ValidationError({"codigo_estoque": "Informe o código de estoque."})
        if self.estoque_atual < 0:
            raise ValidationError({"estoque_atual": "O estoque não pode ser negativo."})
        if self.estoque_minimo < 0:
            raise ValidationError({"estoque_minimo": "O estoque mínimo precisa ser positivo."})

    def save(self, *args, **kwargs):
        """Garante que `clean()` seja executado em toda gravação."""
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def em_alerta(self):
        """Indica se o saldo atual está abaixo ou igual ao mínimo configurado."""
        return self.estoque_atual <= self.estoque_minimo

    def __str__(self):
        return f"{self.nome} ({self.codigo_estoque})"

# Create your models here.
