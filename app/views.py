# imports
from datetime import timezone
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
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
from .forms import LaboratorioForm
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as auth_logout


# Create your views here.
def autenticar_usuario(usuario, senha):
    try:
        usuario = Usuario.objects.get(usuario=usuario)
        if check_password(senha, usuario.senha):
            return usuario  # Autenticação válida
    except Usuario.DoesNotExist:
        pass
    return None  # Falhou na autenticação


@never_cache
def login(request):
    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.session.get('usuario_id'):
        return redirect('inicio')
    
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = autenticar_usuario(usuario, senha)

        if usuario:
            request.session['usuario_id'] = usuario.id
            messages.success(request, f"✅ Bem-vindo(a), {usuario.nome}!")
            
            response = redirect('inicio')
            # Configura headers para evitar cache
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '-1'
            return response
        else:
            messages.error(request, "❌ Usuário ou senha incorretos...")
            return redirect('login')
    
    # Resposta GET com headers anti-cache
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '-1'
    return response


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
    # Se o usuário estiver logado, redireciona para evitar cadastro duplo
    if request.session.get('usuario_id'):
        return redirect('inicio')
        
    if request.method == "POST":
        nome = request.POST.get("nome")
        usuario_input = request.POST.get("usuario")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")
        tipo_usuario = request.POST.get("tipo_usuario", "comum")

        if senha != senha2: 
            messages.error(request, "❌ As senhas não coincidem.")
            return redirect('cadastro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "❌ E-mail já cadastrado.")
            return redirect('cadastro')
        
        if Usuario.objects.filter(usuario=usuario_input).exists():
            messages.error(request, "❌ Nome de usuário já existe")
            return redirect('cadastro')

        senha_hash = make_password(senha)
        usuario = Usuario(
            nome=nome,
            usuario=usuario_input,
            email=email,
            senha=senha_hash,
            tipo_usuario=tipo_usuario
        )
        usuario.save()

        messages.success(request, "✅ Cadastro realizado com sucesso! Faça login.")
        return redirect('login')

    # Garante que a resposta não seja cacheadá
    response = render(request, 'cadastro.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '-1'
    return response

# view para recupera senha
def esqueci_senha(request):
    return render(request, 'esqueci_senha.html')

# view que mostra os laboratorios e
# cadastra ou exclui
def laboratorios_view(request):
    laboratorios = Laboratorio.objects.all()
    
    # Você pode adicionar lógica para filtrar por tipo se necessário
    # labs_informatica = Laboratorio.objects.filter(tipo='informatica')
    # salas_aula = Laboratorio.objects.filter(tipo='sala_aula')
    
    return render(request, 'laboratorios.html', {
        'laboratorios': laboratorios,
        # 'labs_informatica': labs_informatica,
        # 'salas_aula': salas_aula
    })

@never_cache
@login_required
def painel_admin(request):
    usuarios = Usuario.objects.all().exclude(tipo_usuario='admin')
    return render(request, 'partials/painel_admin.html', {'usuarios': usuarios})


def cadastrar_laboratorio(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratório cadastrado com sucesso!')
            return redirect('laboratorios')
    else:
        form = LaboratorioForm()
    return render(request, 'cadastro_laboratorio.html', {'form': form})


def reservas(request):
    return render(request, 'reservas.html')





