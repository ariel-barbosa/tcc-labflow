from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path
from .views import (
    HomeView,
    LaboratorioListView,
    DisponibilidadeView,
    LoginView,
    ReservaCreateView,
    MinhasReservasListView,
    ReservaDeleteView
)



urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # suas outras URLs...


    path('', HomeView.as_view(), name='home'),
    path('laboratorios/', LaboratorioListView.as_view(), name='listar_laboratorios'),
    path('laboratorios/<int:lab_id>/disponibilidade/', DisponibilidadeView.as_view(), name='ver_disponibilidade'),
    path('laboratorios/<int:lab_id>/reservar/', ReservaCreateView.as_view(), name='criar_reserva'),
    path('minhas-reservas/', MinhasReservasListView.as_view(), name='minhas_reservas'),
    path('minhas-reservas/<int:pk>/cancelar/', ReservaDeleteView.as_view(), name='cancelar_reserva'),
]