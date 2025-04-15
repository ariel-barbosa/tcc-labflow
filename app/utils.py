from django.contrib.auth.hashers import check_password
from .models import Usuario

def autenticar_usuario(email, senha):
    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            return usuario
    except Usuario.DoesNotExist:
        return None



from django.shortcuts import redirect
from .models import Usuario

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.tipo_usuario != 'admin':
                return redirect('inicio')  # bloqueia se não for admin
        except Usuario.DoesNotExist:
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper
