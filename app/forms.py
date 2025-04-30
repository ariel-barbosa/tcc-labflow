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

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

Usuario = get_user_model()

class CadastroUsuarioForm(UserCreationForm):
    nome = forms.CharField(
        label='Nome Completo',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    tipo_usuario = forms.ChoiceField(
        choices=[('comum', 'Usuário Comum'), ('admin', 'Administrador')],
        initial='comum',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email', 'tipo_usuario', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação de Senha'

from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )