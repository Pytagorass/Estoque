from django.shortcuts import render

# Create your views here.
def visualizarCarrinho(request):
    return render(request, 'loja/carrinho.html')