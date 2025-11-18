from django.db import models

from produto.models import Produto

# Create your models here.
class Carrinho(models.Model):
    car_id = models.CharField(max_length=250, blank=True)
    date_add = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.car_id
    
# Classe que representará os itens do carrinho
class CarItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # null= o valor True é adicionado automaticamente
    car = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quant = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.produto 