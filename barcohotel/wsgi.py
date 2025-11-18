"""
Configuração WSGI para o projeto Controle de Estoque.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barcohotel.settings")

application = get_wsgi_application()
