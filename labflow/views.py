from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Laboratorio, Reserva
from .forms import ReservaForm
from datetime import datetime, time, date, timedelta

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Seu template personalizado
    # redirect_authenticated_user = True  # Redireciona usuários já logados

class HomeView(TemplateView):
    template_name = 'home.html'
    
    # Descomente se quiser redirecionar usuários logados
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('labflow:listar_laboratorios')
    #     return super().dispatch(request, *args, **kwargs)

class LaboratorioListView(LoginRequiredMixin, ListView):
    model = Laboratorio
    template_name = 'laboratorios.html'
    context_object_name = 'laboratorios'
    ordering = ['nome']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()
        
        for lab in context['laboratorios']:
            lab.reservas_hoje = Reserva.objects.filter(
                laboratorio=lab, 
                data=hoje
            )
        
        return context

class DisponibilidadeView(LoginRequiredMixin, TemplateView):
    template_name = 'labflow/disponibilidade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laboratorio = get_object_or_404(Laboratorio, pk=self.kwargs['lab_id'])
        
        data_selecionada = self.request.GET.get('data', date.today().isoformat())
        try:
            data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        except ValueError:
            data_selecionada = date.today()
        
        reservas = Reserva.objects.filter(
            laboratorio=laboratorio, 
            data=data_selecionada
        ).order_by('hora_inicio')
        
        slots = []
        hora_atual = time(8, 0)
        while hora_atual <= time(18, 0):
            slot = {
                'hora': hora_atual,
                'disponivel': True,
                'reserva': None
            }
            
            for reserva in reservas:
                if reserva.hora_inicio <= hora_atual < reserva.hora_fim:
                    slot['disponivel'] = False
                    slot['reserva'] = reserva
                    break
            
            slots.append(slot)
            hora_atual = (datetime.combine(date.today(), hora_atual) + timedelta(minutes=30)).time()
        
        context.update({
            'laboratorio': laboratorio,
            'data_selecionada': data_selecionada,
            'slots': slots,
            'reservas': reservas,
        })
        return context

class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'labflow/criar_reserva.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'data': self.request.GET.get('data', ''),
            'hora_inicio': self.request.GET.get('hora', ''),
        })
        return initial
    
    def form_valid(self, form):
        form.instance.laboratorio = get_object_or_404(Laboratorio, pk=self.kwargs['lab_id'])
        form.instance.usuario = self.request.user
        
        try:
            form.instance.clean()
            messages.success(self.request, 'Reserva criada com sucesso!')
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('labflow:minhas_reservas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['laboratorio'] = get_object_or_404(Laboratorio, pk=self.kwargs['lab_id'])
        return context

class MinhasReservasListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'labflow/minhas_reservas.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        return Reserva.objects.filter(
            usuario=self.request.user
        ).order_by('-data', '-hora_inicio')

class ReservaDeleteView(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'labflow/cancelar_reserva.html'
    
    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Reserva cancelada com sucesso!')
        return reverse_lazy('labflow:minhas_reservas')