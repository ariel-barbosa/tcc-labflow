from django import forms
from .models import Laboratorio, Reserva

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nome', 'tipo', 'descricao', 'capacidade', 'localizacao', 'imagem', 'disponivel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nome': 'Nome do Laboratório',
            'tipo': 'Tipo de Laboratório',
            'descricao': 'Descrição',
            'capacidade': 'Capacidade',
            'localizacao': 'Localização',
            'imagem': 'Foto do Laboratório',
            'disponivel': 'Disponível para reservas',
        }


from django import forms
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data', 'hora_inicio', 'hora_fim', 'observacao']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().strftime('%Y-%m-%d')
            }),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
        }

from django import forms
from .models import Laboratorio

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'  # Ou liste os campos específicos