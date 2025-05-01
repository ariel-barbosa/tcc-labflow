from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva
from datetime import date, time

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data', 'hora_inicio', 'hora_fim', 'motivo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')
        
        if data and hora_inicio and hora_fim:
            # Verifica se a data não é no passado
            if data < date.today():
                raise ValidationError("Não é possível reservar para datas passadas.")
            
            # Verifica se o horário de fim é depois do horário de início
            if hora_fim <= hora_inicio:
                raise ValidationError("O horário de término deve ser após o horário de início.")
            
            # Verifica se o horário está dentro do funcionamento do laboratório
            if hora_inicio < time(8, 0) or hora_fim > time(18, 0):
                raise ValidationError("O laboratório só está disponível entre 8h e 18h.")