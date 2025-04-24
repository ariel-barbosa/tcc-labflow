from django.shortcuts import redirect
from django.urls import path
from django.conf.urls.static import static  # Importe a função static
from setup import settings
from . import views

urlpatterns = [
    # login, cadastro e logOut no sistema
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.sair, name='logout'),  # Changed from 'sair' to 'logout'
    
    # agendamentos
    path('reservas/', views.reservas, name='reservas'),
    
    # laboratorios
    path('laboratorios/', views.laboratorios_view, name='laboratorios'),
    path('laboratorios/cadastrar/', views.cadastrar_laboratorio, name='cadastrar_laboratorio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

