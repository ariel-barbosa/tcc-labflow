from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django

# Create your views here.
@never_cache
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            messages.success(request, f"✅ Login realizado com sucesso!", {user.username})  # Mensagem de sucesso
            return redirect('inicio')  # Redireciona após o login
        else:
            messages.error(request, "❌ Usuário ou senha incorretos...")  # Mensagem de erro
            return redirect('login')  # Retorna ao login