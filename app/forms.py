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

from django import forms
from .models import Reserva
import datetime 

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['laboratorio', 'data', 'hora_inicio', 'hora_fim', 'motivo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
        }