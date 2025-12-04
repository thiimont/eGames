from .models import Pagina

def pagina(request):
    return { 'info': Pagina.objects.first() }