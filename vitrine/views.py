from django.shortcuts import get_object_or_404, render

from categoria.models import Categoria
from produto.models import Produto

# Create your views here.

def visualizarVitrine(request, categoria_slug=None):
    produtos = None
    categorias = None
    
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.all().filter(categoria = categorias, esta_disponivel=True)
    else:
        produtos = Produto.objects.all().filter(esta_disponivel=True).order_by('id')

    contexto = {
        'produtos': produtos
    }

    return render(request, 'index.html', contexto)
