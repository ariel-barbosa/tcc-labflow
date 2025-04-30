from datetime import datetime
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Reserva, Usuario, Laboratorio
from .forms import LaboratorioForm, ReservaForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Laboratorio, Reserva
from .forms import LaboratorioForm, ReservaForm

# Decorator para verificar admin
def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_usuario == 'admin':
            return function(request, *args, **kwargs)
        messages.error(request, "Acesso restrito a administradores")
        return redirect('laboratorios')
    return wrapper

# View de Laboratórios
@method_decorator(login_required, name='dispatch')
class LaboratorioListView(ListView):
    model = Laboratorio
    template_name = 'laboratorios/laboratorios.html'
    context_object_name = 'laboratorios'

# View para criar reserva
@login_required
def criar_reserva(request, lab_id):
    laboratorio = get_object_or_404(Laboratorio, id=lab_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.laboratorio = laboratorio
            reserva.usuario = request.user
            
            try:
                reserva.full_clean()  # Valida os dados (incluindo conflitos de horário)
                reserva.save()
                messages.success(request, "Reserva realizada com sucesso!")
                return redirect('minhas_reservas')
            except ValidationError as e:
                messages.error(request, f"Erro na reserva: {', '.join(e.messages)}")
    else:
        form = ReservaForm(initial={'laboratorio': laboratorio})
    
    return render(request, 'reservas/criar_reserva.html', {
        'form': form,
        'laboratorio': laboratorio
    })

# Views administrativas
@login_required
@admin_required
def editar_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    
    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            messages.success(request, "Laboratório atualizado com sucesso!")
            return redirect('laboratorios')
    else:
        form = LaboratorioForm(instance=laboratorio)
    
    return render(request, 'laboratorios/editar_laboratorio.html', {
        'form': form,
        'laboratorio': laboratorio
    })

@login_required
@admin_required
def excluir_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    
    if request.method == 'POST':
        laboratorio.delete()
        messages.success(request, "Laboratório excluído com sucesso!")
        return redirect('laboratorios')
    
    return render(request, 'laboratorios/excluir_laboratorio.html', {
        'laboratorio': laboratorio
    })


# Authentication Utilities
def autenticar_usuario(usuario, senha):
    try:
        usuario = Usuario.objects.get(usuario=usuario)
        if check_password(senha, usuario.senha):
            return usuario
    except Usuario.DoesNotExist:
        pass
    return None

def verificar_admin(usuario):
    """Verifica se o usuário é administrador"""
    if not usuario.tipo_usuario == 'admin':
        raise PermissionDenied

# Authentication Views
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .forms import LoginForm  # Você precisará criar este formulário

Usuario = get_user_model()

@method_decorator(never_cache, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'inicio'  # Será sobrescrito no form_valid

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('usuario_id'):
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['usuario']
        senha = form.cleaned_data['senha']

        try:
            usuario = Usuario.objects.get(username=username)
            if check_password(senha, usuario.password):
                self.request.session['usuario_id'] = usuario.id
                messages.success(self.request, f"✅ Bem-vindo(a), {usuario.first_name}!")
                return redirect(self.get_success_url())
            
            messages.error(self.request, "❌ Senha incorreta...")
        except Usuario.DoesNotExist:
            messages.error(self.request, "❌ Usuário não encontrado...")
        
        return redirect('login')

    def get_success_url(self):
        return self.success_url

@never_cache
def sair(request):
    request.session.flush()
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    return response

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from .models import Usuario
from .forms import CadastroUsuarioForm  # Você precisará criar este form

@method_decorator(never_cache, name='dispatch')
class CadastroUsuarioView(CreateView):
    model = Usuario
    form_class = CadastroUsuarioForm
    template_name = 'templates/cadastro_usuario.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('usuario_id'):
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if Usuario.objects.filter(email=form.cleaned_data['email']).exists():
            form.add_error('email', 'Este e-mail já está cadastrado.')
            return self.form_invalid(form)
            
        try:
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['nome']
            user.tipo_usuario = form.cleaned_data['tipo_usuario']
            user.save()
            messages.success(self.request, "✅ Cadastro realizado com sucesso! Faça login.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"❌ Erro ao cadastrar: {str(e)}")
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '-1'
        return response
    

def esqueci_senha(request):
    return render(request, 'esqueci_senha.html')

# Main Views
@never_cache
def inicio(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        response = render(request, 'inicio.html', {'usuario': usuario})
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
        return response
    except Usuario.DoesNotExist:
        del request.session['usuario_id']
        return redirect('login')

# Laboratory Views
@method_decorator(never_cache, name='dispatch')
class LaboratorioListView(ListView):
    model = Laboratorio
    template_name = 'laboratorios/laboratorios.html'
    context_object_name = 'laboratorios'
    
    def get_queryset(self):
        return Laboratorio.objects.all().order_by('nome')

@never_cache
@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'admin')
def cadastrar_laboratorio(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratório cadastrado com sucesso!')
            return redirect('laboratorios')
    else:
        form = LaboratorioForm()
    
    return render(request, 'laboratorios/cadastrar.html', {'form': form})

@never_cache
@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'admin')
def editar_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            messages.success(request, "Laboratório atualizado com sucesso!")
            return redirect('laboratorios')
    else:
        form = LaboratorioForm(instance=laboratorio)
    
    return render(request, 'laboratorios/editar.html', {'form': form})

@never_cache
@login_required
@user_passes_test(lambda u: u.tipo_usuario == 'admin')
def excluir_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    if request.method == 'POST':
        laboratorio.delete()
        messages.success(request, "Laboratório excluído com sucesso!")
        return redirect('laboratorios')
    
    return render(request, 'laboratorios/excluir.html', {'laboratorio': laboratorio})

# Reservation Views
@never_cache
@login_required
def reservas_view(request):
    laboratorios = Laboratorio.objects.filter(disponivel=True)
    return render(request, 'reservas/listar.html', {'laboratorios': laboratorios})

@never_cache
@login_required
def criar_reserva(request, lab_id):
    laboratorio = get_object_or_404(Laboratorio, id=lab_id)
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.laboratorio = laboratorio
            reserva.usuario = usuario
            
            try:
                reserva.full_clean()
                reserva.save()
                messages.success(request, "Reserva realizada com sucesso!")
                return redirect('minhas_reservas')
            except ValidationError as e:
                messages.error(request, f"Erro na reserva: {', '.join(e.messages)}")
    else:
        form = ReservaForm(initial={
            'laboratorio': laboratorio,
            'data': datetime.date.today()
        })
    
    return render(request, 'reservas/form.html', {
        'form': form,
        'laboratorio': laboratorio
    })

@never_cache
@login_required
def minhas_reservas(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    reservas = Reserva.objects.filter(usuario=usuario).order_by('data', 'hora_inicio')
    return render(request, 'reservas/minhas.html', {'reservas': reservas})

@never_cache
@login_required
def cancelar_reserva(request, pk):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    reserva = get_object_or_404(Reserva, pk=pk, usuario=usuario)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('minhas_reservas')
    
    return render(request, 'reservas/cancelar.html', {'reserva': reserva})