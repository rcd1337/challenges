from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import Client, Ad
from .util import max_clicks, max_shares, max_views


def index(request):
    return render(request, "sistema/index.html")

def ad(request):
    
    if request.method == 'POST':

        # Data validation
        ad_name = request.POST['name']
        if ad_name == "":
            messages.error(request, f'Nome inválido.')
            return HttpResponseRedirect(reverse('ad'))

        try:
            client = Client.objects.get(pk=request.POST['client_id'])
        except Client.DoesNotExist:
            messages.error(request, f'Cliente informado não foi encontrado no banco de dados.')
            return HttpResponseRedirect(reverse('ad'))

        try:
            start_date =  datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, f'Data inválida.')
            return HttpResponseRedirect(reverse('ad'))
        
        if end_date <= start_date:
            messages.error(request, f'Data de término deve ser superior a de início.')
            return HttpResponseRedirect(reverse('ad'))

        try:
            investment = float(request.POST['investment'])
        except ValueError:
            messages.error(request, f'Valor inválido.')
            return HttpResponseRedirect(reverse('ad'))

        delta = end_date - start_date
        days = delta.days
        investment_total = investment * days

        # Attempts to save data to database
        try:
            new_ad = Ad(name=ad_name, client=client, start_date=start_date, end_date=end_date, days=days, investment_day=investment, investment_total=investment_total)
            new_ad.save()
            messages.error(request, f'Anúncio cadastrado com sucesso.')
        except Exception:
            messages.error(request, f'Não foi possível cadastrar anúncio.')
            return HttpResponseRedirect(reverse('ad'))
    
    clients = Client.objects.all()
    return render(request, "sistema/ad.html", {
        'clients': clients
    })

def client(request):
    if request.method == 'POST':
        name = request.POST['name']

        if not name:
            messages.error(request, f'Nome inválido.')
            return render(request, "sistema/client.html")

        # Checks if client's name is already registered
        try:
            Client.objects.get(name=name)
            messages.error(request, f'Cliente "{name}" já cadastrado.')
            return render(request, "sistema/client.html")
        except Client.DoesNotExist:
            pass
        
        # Attempts to register new client to database
        try:
            new_client = Client(name=name)
            new_client.save()
            messages.error(request, f'Cliente "{name}" cadastrado com sucesso.')
        except Exception:
            messages.error(request, f"Cadastro não efetuado.")
            return render(request, "sistema/client.html")

    return render(request, "sistema/client.html")

def report(request):
    if request.method == 'POST':

        # Data validation
        try:
            start_date =  datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, f'Data inválida.')
            return HttpResponseRedirect(reverse('reports'))
        
        if end_date <= start_date:
            messages.error(request, f'Data de término deve ser superior a de início.')
            return HttpResponseRedirect(reverse('reports'))
        
        try:
            ad = Ad.objects.get(pk=request.POST['ad_id'])
        except Ad.DoesNotExist:
            messages.error(request, f'Anúcio não encontrado.')
            return HttpResponseRedirect(reverse('reports'))

        delta = end_date - start_date
        requested_days = delta.days
        requested_investment = float(ad.investment_day) * float(requested_days)
        views_invested = requested_investment * float(30)

        return render(request, "sistema/report.html", {
            'ad': ad,
            'start_date': start_date,
            'end_date': end_date,
            'investment': "R$ {:,.2f}".format(requested_investment),
            'max_clicks': max_clicks(views_invested),
            'max_shares': max_shares(views_invested),
            'max_views': max_views(views_invested)
        })
    else:
        return HttpResponseRedirect(reverse('reports'))

def reports(request):
    clients = Client.objects.all()

    if request.method == 'POST':
        client = Client.objects.get(pk=request.POST['client_id'])
        ads = client.ads.all()
        
        empty = False
        if not ads:
            empty = True

        return render(request, "sistema/reports.html", {
            'clients': clients,
            'ads': ads,
            'client': client,
            'empty': empty
        })

    return render(request, "sistema/reports.html", {
        'clients': clients
    })