from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Le viste base vanno qui.
from django.template import RequestContext
from anagrafica.models import Sede
from autenticazione.funzioni import pagina_pubblica
from base.forms import ModuloRecuperaPassword


@pagina_pubblica
def index(request):
    contesto = {
        'numero_comitati': Sede.objects.count(),
    }
    return 'base_home.html', contesto

@pagina_pubblica
def manutenzione(request):
    """
    Mostra semplicemente la pagina di manutenzione ed esce.
    """
    return 'base_manutenzione.html'

@pagina_pubblica
def recupera_password(request):
    """
    Mostra semplicemente la pagina di recupero password.
    """
    if request.method == 'POST':
        modulo = ModuloRecuperaPassword(request.POST)
        if modulo.is_valid():
            pass
            # TODO RECUPERO
    else:
        contesto = {
            'modulo': ModuloRecuperaPassword(),
        }
        return 'base_recupera_password.html', contesto

@pagina_pubblica
def informazioni(request):
    """
    Mostra semplicemente la pagina diinformazioni ed esce.
    """
    return 'base_informazioni.html'

@pagina_pubblica
def aggiornamenti(request):
    """
    Mostra semplicemente la pagina degli aggiornamenti ed esce.
    """
    return 'base_informazioni_aggiornamenti.html'

@pagina_pubblica
def sicurezza(request):
    """
    Mostra semplicemente la pagina degli aggiornamenti ed esce.
    """
    return 'base_informazioni_sicurezza.html'

@pagina_pubblica
def condizioni(request):
    """
    Mostra semplicemente la pagina delle condizioni ed esce.
    """
    return 'base_informazioni_condizioni.html'