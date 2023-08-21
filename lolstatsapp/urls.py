from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),             # Página de inicio
    path('search/', views.search, name='search'),  # Página de búsqueda y resultados
]
