from django.urls import path
from .views import CadastroUsuarioView, LaboratorioListView, CadastroUsuarioView, LoginView
from django.contrib.auth import views as auth_views
from .views import (
    # Views de Autenticação
    esqueci_senha,
    inicio,
    sair,
    
    # Views de Laboratórios (função)
    # laboratorios_view,  # Substitui LaboratorioListView
    cadastrar_laboratorio,
    editar_laboratorio,
    excluir_laboratorio,
    
    # Views de Reservas
    reservas_view,
    criar_reserva,
    minhas_reservas,
    cancelar_reserva
)
from app import views

urlpatterns = [
    # Autenticação
    # path('', login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroUsuarioView.as_view(), name='cadastro'),
    path('esqueci-senha/', esqueci_senha, name='esqueci_senha'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', sair, name='logout'),
    
    # Laboratórios (agora usando a função laboratorios_view)
    # path('laboratorios/', laboratorios_view, name='laboratorios'),
    path('laboratorios/', views.LaboratorioListView.as_view(), name='laboratorios'),
    path('laboratorios/editar/<int:pk>/', views.editar_laboratorio, name='editar_laboratorio'),
    path('laboratorios/excluir/<int:pk>/', views.excluir_laboratorio, name='excluir_laboratorio'),
    path('laboratorios/<int:lab_id>/reservar/', views.criar_reserva, name='criar_reserva'),
    
    path('reservas/', reservas_view, name='reservas'),
    path('laboratorios/<int:lab_id>/reservar/', criar_reserva, name='criar_reserva'),
    path('reservas/minhas/', minhas_reservas, name='minhas_reservas'),
    path('reservas/cancelar/<int:pk>/', cancelar_reserva, name='cancelar_reserva'),

    path('laboratorios/<int:lab_id>/reservar/', criar_reserva, name='criar_reserva'),

    
]