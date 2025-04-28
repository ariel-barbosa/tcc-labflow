from django import forms
from .models import Laboratorio, Equipamento, Funcionamento, Reserva

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'

class FuncionamentoForm(forms.ModelForm):
    class Meta:
        model = Funcionamento
        fields = '__all__'

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'