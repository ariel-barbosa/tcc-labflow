# imports
from datetime import timezone
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reserva, Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.hashers import check_password
from .models import Usuario
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .models import Usuario
from .utils import admin_required, autenticar_usuario  # se você quiser separar a função em um arquivo utils.py
from django.shortcuts import render
from .models import Laboratorio
from .forms import LaboratorioForm, ReservaForm
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Laboratorio
from .forms import LaboratorioForm
from django.views.generic import ListView
from .models import Laboratorio
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def autenticar_usuario(usuario, senha):
    try:
        usuario = Usuario.objects.get(usuario=usuario)
        if check_password(senha, usuario.senha):
            return usuario  # Autenticação válida
    except Usuario.DoesNotExist:
        pass
    return None  # Falhou na autenticação

@csrf_protect
@never_cache
def login(request):
    if request.session.get('usuario_id'):
        return redirect('inicio')
    
    if request.method == "POST":
        username = request.POST.get('usuario')  # Recebe do formulário como 'usuario'
        senha = request.POST.get('senha')

        # Autenticação usando o campo username
        try:
            usuario = Usuario.objects.get(username=username)  # Filtra por username
            if check_password(senha, usuario.password):
                request.session['usuario_id'] = usuario.id
                messages.success(request, f"✅ Bem-vindo(a), {usuario.first_name}!")
                return redirect('inicio')
            else:
                messages.error(request, "❌ Senha incorreta...")
        except Usuario.DoesNotExist:
            messages.error(request, "❌ Usuário não encontrado...")
        
        return redirect('login')
    
    return render(request, 'login.html')


@never_cache
def sair(request):
    # Limpa todos os dados da sessão
    request.session.flush()
    
    # Redireciona para login com headers anti-cache
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    return response

@never_cache
def inicio(request):
    # Verifica se o usuário está autenticado
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    try:
        # Obtém o usuário da sessão
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        
        # Cria a resposta com headers anti-cache
        response = render(request, 'inicio.html', {'usuario': usuario})
        
        # Configura headers para evitar cache no navegador
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
        
        return response
    
    except Usuario.DoesNotExist:
        # Se o usuário não existe mais no banco de dados
        del request.session['usuario_id']
        return redirect('login')


@never_cache
def cadastro(request):
    if request.session.get('usuario_id'):
        return redirect('inicio')
        
    if request.method == "POST":
        # Obtenha os dados do formulário
        nome = request.POST.get("nome")
        username = request.POST.get("usuario")  # Corresponde ao name="usuario" do formulário
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")
        tipo_usuario = request.POST.get("tipo_usuario", "comum")

        # Validações
        if senha != senha2:
            messages.error(request, "❌ As senhas não coincidem.")
            return redirect('cadastro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "❌ E-mail já cadastrado.")
            return redirect('cadastro')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "❌ Nome de usuário já existe")
            return redirect('cadastro')

        # Crie o usuário usando o método create_user do Django
        try:
            username = Usuario.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=nome,  # Usamos first_name para o nome completo
                tipo_usuario=tipo_usuario
            )
            messages.success(request, "✅ Cadastro realizado com sucesso! Faça login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"❌ Erro ao cadastrar: {str(e)}")
            return redirect('cadastro')

    response = render(request, 'cadastro.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '-1'
    return response

# view para recupera senha
def esqueci_senha(request):
    return render(request, 'esqueci_senha.html')
from django.core.exceptions import PermissionDenied

def verificar_admin(usuario):
    """Verifica se o usuário é administrador"""
    if not usuario.tipo_usuario == 'admin':
        raise PermissionDenied


@never_cache
@login_required
def laboratorios_view(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        laboratorios = Laboratorio.objects.all()
        
        return render(request, 'laboratorios/laboratorios.html', {
            'laboratorios': laboratorios,
            'eh_admin': usuario.tipo_usuario == 'admin'
        })
    except Exception as e:
        messages.error(request, f"Erro ao carregar laboratórios: {str(e)}")
        return redirect('inicio')


@never_cache
@login_required
def cadastrar_laboratorio(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    verificar_admin(usuario)
    
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
def editar_laboratorio(request, pk):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    verificar_admin(usuario)
    
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
def excluir_laboratorio(request, pk):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    verificar_admin(usuario)
    
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    if request.method == 'POST':
        laboratorio.delete()
        messages.success(request, "Laboratório excluído com sucesso!")
        return redirect('laboratorios')
    
    return render(request, 'laboratorios/excluir.html', {'laboratorio': laboratorio})

@never_cache
@login_required
def reservas_view(request):
    laboratorios = Laboratorio.objects.filter(disponivel=True)
    return render(request, 'reservas/listar.html', {'laboratorios': laboratorios})

@never_cache
@login_required
def criar_reserva(request, lab_id):
    laboratorio = get_object_or_404(Laboratorio, id=lab_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.laboratorio = laboratorio
            reserva.usuario = Usuario.objects.get(id=request.session['usuario_id'])
            
            # Verifica conflito de horário
            conflitos = Reserva.objects.filter(
                laboratorio=laboratorio,
                data=reserva.data,
                hora_inicio__lt=reserva.hora_fim,
                hora_fim__gt=reserva.hora_inicio
            )
            
            if conflitos.exists():
                messages.error(request, "Já existe reserva neste horário")
            else:
                reserva.save()
                messages.success(request, "Reserva realizada com sucesso!")
                return redirect('minhas_reservas')
    else:
        form = ReservaForm()
    
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