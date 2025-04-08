# imports
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
from .utils import autenticar_usuario  # se você quiser separar a função em um arquivo utils.py
from django.contrib.auth import logout



# Create your views here.
def autenticar_usuario(email, senha):
    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            return usuario  # Autenticação válida
    except Usuario.DoesNotExist:
        pass
    return None  # Falhou na autenticação

@never_cache
def inicio(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    return render(request, 'inicio.html')


# cadastrar usuario
def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        usuario = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")

        if senha != senha2:
            messages.error(request, "❌ As senhas não coincidem.")
            return redirect('cadastro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "❌ E-mail já cadastrado.")
            return redirect('cadastro')
        
        if Usuario.objects.filter(username=usuario).exists():
            messages.error(request, "❌ username já existe")
            return redirect('cadastro')

        senha_hash = make_password(senha)
        usuario = Usuario(nome=nome, username=usuario, email=email, senha=senha_hash)
        usuario.save()

        messages.success(request, "✅ Cadastro realizado com sucesso! Faça login.")
        return redirect('login')

    return render(request, 'cadastro.html')


@never_cache
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = autenticar_usuario(email, senha)

        if usuario:
            request.session['usuario_id'] = usuario.id
            messages.success(request, f"✅ Bem-vindo(a), {usuario.nome}!")
            return redirect('inicio')
        else:
            messages.error(request, "❌ Usuário ou senha incorretos...")
            return redirect('login')

# view de log out
@never_cache
def sair(request):
    logout(request)
    return redirect('login')


def esqueci_senha(request):
    return render(request, 'esqueci_senha.html')
