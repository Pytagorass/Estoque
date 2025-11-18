from decimal import Decimal

from django.test import TestCase

from .models import Item, Movimentacao


class MovimentacaoTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(nome="Água", codigo_estoque="AGUA01", unidade="UN", estoque_minimo=5)

    def test_saida_nao_pode_passar_estoque(self):
        with self.assertRaises(Exception):
            Movimentacao.objects.create(
                item=self.item,
                tipo="SAIDA",
                quantidade=Decimal("1"),
                responsavel="Teste",
            )

    def test_entrada_atualiza_estoque(self):
        Movimentacao.objects.create(item=self.item, tipo="ENTRADA", quantidade=Decimal("10"), responsavel="Teste")
        self.item.refresh_from_db()
        self.assertEqual(self.item.estoque_atual, Decimal("10"))
