# app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Laboratorio, Equipamento, Funcionamento, Reserva

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Laboratorio)
admin.site.register(Equipamento)
admin.site.register(Funcionamento)
admin.site.register(Reserva)