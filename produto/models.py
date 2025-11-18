from django.db import models
from django.urls import reverse
from categoria.models import Categoria
# Create your models here.
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=200, unique=True)
    descricao = models.CharField(max_length=300, blank=True)
    preco = models.DecimalField(max_digits=11, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='fotos/produtos', blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    # slug = AutoSlugFiled(populate_from ='produto_nome', editable =False, unique=True, always)
    esta_disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.produto_nome
    
    # este método fará o redirecionamento baseado no nome da URL disponível no projeto
    # e nos argumentos que serão passados para a URL
    def get_url(self):
        return reverse('detalhar_produto', args=[self.categoria.slug, self.slug])