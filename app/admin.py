from django.contrib import admin
from .models import Usuario, Laboratorio, Equipamento, Funcionamento, Reserva

# Remova qualquer classe LaboratorioAdmin se existir
# e use apenas o registro básico se não precisar de customização

admin.site.register(Usuario)
admin.site.register(Laboratorio)
admin.site.register(Equipamento)
admin.site.register(Funcionamento)
admin.site.register(Reserva)