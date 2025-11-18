
from django.urls import path

from vitrine import views




urlpatterns = [
    path('', views.visualizarVitrine, name='vitrine'),
    path('<slug:categoria_slug>/', views.visualizarVitrine, name='produtos_por_categoria'),
]