from django.contrib.auth.views import LoginView, LogoutView

from ..forms import LoginForm


class LoginPageView(LoginView):
    """Encapsula o formulário de autenticação padrão da aplicação."""
    template_name = "conta/login.html"
    form_class = LoginForm


class LogoutPageView(LogoutView):
    """Apenas finaliza a sessão e redireciona para a tela de login."""
    next_page = "controle:login"
