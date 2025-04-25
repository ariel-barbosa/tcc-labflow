from django.urls import path
from .views import (
    # Views de Autenticação
    login,
    cadastro,
    esqueci_senha,
    inicio,
    sair,
    
    # Views de Laboratórios (função)
    laboratorios_view,  # Substitui LaboratorioListView
    cadastrar_laboratorio,
    editar_laboratorio,
    excluir_laboratorio,
    
    # Views de Reservas
    reservas_view,
    criar_reserva,
    minhas_reservas,
    cancelar_reserva
)

urlpatterns = [
    # Autenticação
    path('', login, name='login'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('esqueci-senha/', esqueci_senha, name='esqueci_senha'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', sair, name='logout'),
    
    # Laboratórios (agora usando a função laboratorios_view)
    path('laboratorios/', laboratorios_view, name='laboratorios'),  # Removido .as_view()
    path('laboratorios/cadastrar/', cadastrar_laboratorio, name='cadastrar_laboratorio'),
    path('laboratorios/editar/<int:pk>/', editar_laboratorio, name='editar_laboratorio'),
    path('laboratorios/excluir/<int:pk>/', excluir_laboratorio, name='excluir_laboratorio'),
    
    # Reservas
    path('reservas/', reservas_view, name='reservas'),
    path('reservas/nova/<int:lab_id>/', criar_reserva, name='criar_reserva'),
    path('reservas/minhas/', minhas_reservas, name='minhas_reservas'),
    path('reservas/cancelar/<int:pk>/', cancelar_reserva, name='cancelar_reserva'),
]