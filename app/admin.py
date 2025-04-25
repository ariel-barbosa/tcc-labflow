from django.contrib import admin
from .models import Laboratorio, Reserva

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'capacidade', 'localizacao', 'disponivel')
    list_filter = ('tipo', 'disponivel')
    search_fields = ('nome', 'localizacao')
    list_editable = ('disponivel',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('laboratorio', 'usuario', 'data', 'hora_inicio', 'hora_fim', 'data_criacao')
    list_filter = ('data', 'laboratorio')
    search_fields = ('laboratorio__nome', 'usuario__nome')
    date_hierarchy = 'data'