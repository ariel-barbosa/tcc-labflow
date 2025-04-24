from django.shortcuts import redirect
from django.urls import path
from django.conf.urls.static import static  # Importe a função static
from setup import settings
from . import views
from django.urls import path
from .views import (
    LaboratorioListView,
    LaboratorioCreateView,
    LaboratorioUpdateView,
    LaboratorioDeleteView,
    ReservaListView
)

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

    path('laboratorios/', LaboratorioListView.as_view(), name='laboratorios_listar'),
    path('laboratorios/novo/', LaboratorioCreateView.as_view(), name='laboratorios_criar'),
    path('laboratorios/editar/<int:pk>/', LaboratorioUpdateView.as_view(), name='laboratorios_editar'),
    path('laboratorios/excluir/<int:pk>/', LaboratorioDeleteView.as_view(), name='laboratorios_excluir'),

    path('reservas/', ReservaListView.as_view(), name='reservas'),
    path('reservas/novo/<int:lab_id>/', views.criar_reserva, name='criar_reserva'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

