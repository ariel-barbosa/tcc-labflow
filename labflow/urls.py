from django.urls import path
from .views import (
    HomeView,
    LaboratorioListView,
    DisponibilidadeView,
    ReservaCreateView,
    MinhasReservasListView,
    ReservaDeleteView
)

app_name = 'labflow'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('laboratorios/', LaboratorioListView.as_view(), name='listar_laboratorios'),
    path('laboratorios/<int:lab_id>/disponibilidade/', DisponibilidadeView.as_view(), name='ver_disponibilidade'),
    path('laboratorios/<int:lab_id>/reservar/', ReservaCreateView.as_view(), name='criar_reserva'),
    path('minhas-reservas/', MinhasReservasListView.as_view(), name='minhas_reservas'),
    path('minhas-reservas/<int:pk>/cancelar/', ReservaDeleteView.as_view(), name='cancelar_reserva'),
]