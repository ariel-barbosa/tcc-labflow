from django.contrib import admin
from .models import Laboratorio, Equipamento, Reserva

class EquipamentoInline(admin.TabularInline):
    model = Equipamento
    extra = 1

class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nome', 'numero')
    inlines = [EquipamentoInline]

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('laboratorio', 'usuario', 'data', 'hora_inicio', 'hora_fim')
    list_filter = ('laboratorio', 'usuario', 'data')
    search_fields = ('laboratorio__nome', 'usuario__username', 'motivo')

admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(Reserva, ReservaAdmin)