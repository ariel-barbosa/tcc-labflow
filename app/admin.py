from django.contrib import admin
from .models import Laboratorio

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'capacidade', 'localizacao')
    list_filter = ('tipo',)
    search_fields = ('nome', 'localizacao')