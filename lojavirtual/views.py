from django.http import HttpResponse
from django.shortcuts import render

from produto.models import Produto


def visualizarHome(request):
    
    # criando  objeto produtos para enviar a lista à pagina de produtos
    produtos = Produto.objects.all().filter(esta_disponivel=True)
    
    #criando um objeto do tipo mapa compativel com o formato JSON
    contexto ={
        'produtos': produtos
    }
    
    return render(request, 'index.html', contexto)
