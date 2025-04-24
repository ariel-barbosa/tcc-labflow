from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Adiciona headers para evitar cache
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
        return response

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Se usando o sistema de auth padrão do Django
            last_activity = request.session.get('last_activity')
            if last_activity:
                if timezone.now() - last_activity > timedelta(minutes=30):
                    request.session.flush()
                    return redirect('login')
            
            request.session['last_activity'] = timezone.now()
        
        elif 'usuario_id' in request.session:
            # Se usando seu sistema de sessão personalizado
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = timezone.datetime.fromisoformat(last_activity_str)
                if timezone.now() - last_activity > timedelta(minutes=30):
                    request.session.flush()
                    return redirect('login')
            
            request.session['last_activity'] = str(timezone.now())

        return self.get_response(request)