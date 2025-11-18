"""
Configuração ASGI para o projeto Controle de Estoque.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barcohotel.settings")

application = get_asgi_application()
