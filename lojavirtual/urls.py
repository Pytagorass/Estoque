from django.contrib import admin
from django.urls import include, path

from lojavirtual import settings
from django.conf.urls.static import static

from vitrine import views
import vitrine

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.visualizarVitrine, name='home'),
    path('produtos/', include('produto.urls')),
    path('vitrine/', include('vitrine.urls')),
    path('carrinho/', include('carrinho.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
