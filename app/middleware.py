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
    

from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pular middleware para URLs do admin
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        try:
            if 'usuario_id' in request.session:
                last_activity_str = request.session.get('last_activity')
                
                if last_activity_str:
                    # Converter string para datetime de forma robusta
                    try:
                        if isinstance(last_activity_str, str):
                            # Remove microsegundos se existirem
                            if '.' in last_activity_str:
                                last_activity_str = last_activity_str.split('.')[0]
                            
                            # Tenta parsear com e sem 'T'
                            try:
                                last_activity = datetime.fromisoformat(last_activity_str)
                            except ValueError:
                                last_activity = datetime.strptime(last_activity_str, "%Y-%m-%d %H:%M:%S")
                        else:
                            last_activity = last_activity_str

                        # Verifica timeout (30 minutos)
                        if (timezone.now() - last_activity) > timedelta(minutes=30):
                            request.session.flush()
                            return redirect('login')
                    
                    except (ValueError, TypeError) as e:
                        # Se falhar na conversão, limpa a sessão
                        request.session.flush()
                        return redirect('login')

                # Atualiza a última atividade
                request.session['last_activity'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        except Exception as e:
            # Log do erro para debug
            print(f"Erro no middleware: {str(e)}")
            pass

        return self.get_response(request)