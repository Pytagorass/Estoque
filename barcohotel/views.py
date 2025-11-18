from django.shortcuts import redirect


def home(request):
    """Redireciona para o painel principal."""
    return redirect("controle:relatorio")
