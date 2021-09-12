from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import Client, Currency, Operation


def index(request):
    return render(request, "manager/index.html")


def add_client(request):
    if request.method == 'POST':
        name = request.POST['name']

        if not name:
            messages.error(request, f'Nome inválido.')
            return render(request, "manager/add_client.html", status=400)

        # Checks if client's name is already registered
        try:
            Client.objects.get(name=name)
            messages.error(request, f'Cliente "{name}" já cadastrado.')
            return render(request, "manager/add_client.html", status=400)
        except Client.DoesNotExist:
            pass
        
        # Attempts to register new client to database
        try:
            new_client = Client(name=name)
            new_client.save()
            messages.success(request, f'Cliente "{name}" cadastrado com sucesso.')
            return render(request, "manager/add_client.html", status=201)
        except Exception:
            messages.error(request, f"Cadastro não efetuado.")
            return render(request, "manager/add_client.html", status=400)

    return render(request, "manager/add_client.html")


def add_operation(request):
    if request.method == "POST":
        fee = 0.10

        # Validates client
        try:
            client = Client.objects.get(name=request.POST['client_name'])
        except Client.DoesNotExist:
            messages.error(request, f'Cliente não encontrado.')
            return HttpResponseRedirect(reverse('add_operation'))
        
        # Validates source_currency
        try:
            source_currency = Currency.objects.get(pk=request.POST['source_currency_id'])
        except Currency.DoesNotExist:
            messages.error(request, f'Moeda origem inválida.')
            return HttpResponseRedirect(reverse('add_operation'))

        # Validates target_currency
        try:
            target_currency = Currency.objects.get(pk=request.POST['target_currency_id'])
        except Currency.DoesNotExist:
            messages.error(request, f'Moeda destino inválida.')
            return HttpResponseRedirect(reverse('add_operation'))

        # Validates amount
        try:
            amount = float(request.POST['amount'])
        except ValueError:
            messages.error(request, f'Valor inválido.')
            return HttpResponseRedirect(reverse('add_operation'))

        # Converts currency
        sourceIndex = float(source_currency.indexed_value)
        
        # Converted in dollars 
        converted_amount = amount / sourceIndex
        fee_amount = converted_amount * fee
        total = converted_amount - fee_amount

        # Attempts to save to database
        try:
            new_operation = Operation(client=client, source_currency=source_currency,
            target_currency=target_currency, source_amount=amount, converted_amount=converted_amount,
            fee_amount=fee_amount, total=total)
            new_operation.save()
            messages.success(request, f'Operação cadastrada com sucesso.')
            return HttpResponseRedirect(reverse('add_operation'))
        except Exception:
            messages.error(request, f'Não foi possível cadastrar a operação.')
            return HttpResponseRedirect(reverse('add_operation'))

    clients = Client.objects.all().order_by('name')
    currencies = Currency.objects.all()
    return render(request, "manager/add_operation.html", {
        'clients': clients,
        'currencies': currencies
    })


def reports(request):
    clients = Client.objects.all().order_by('name')
    all_operations = Operation.objects.all()

    if request.method == 'POST':

        # Client validation
        if not request.POST['client_name']:
            all_clients = True
        else:
            try:
                all_clients = False
                client = Client.objects.get(name=request.POST['client_name'])
            except Client.DoesNotExist:
                messages.error(request, f'Cliente não encontrado.')
                return HttpResponseRedirect(reverse('reports'))

        # Date validation
        try:
            start_date =  datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
            end_date_plus_one = end_date + datetime.timedelta(days=1)
        except ValueError:
            messages.error(request, f'Data inválida.')
            return HttpResponseRedirect(reverse('reports'))
        
        # Returns all clients if 'client_name' form is empty
        if not all_clients:
            operations = client.operations.filter(created_on__range=[start_date, end_date_plus_one]).order_by('-id')
            client = client.name
        else:
            operations = all_operations.filter(created_on__range=[start_date, end_date_plus_one]).order_by('-id')
            client = None
        
        period_total = operations.aggregate(Sum('converted_amount'), Sum('fee_amount'), Sum('total'),)

        empty = False
        if not operations:
            empty = True

        return render(request, "manager/reports.html", {
            'total_conversions': period_total['converted_amount__sum'],
            'total_fees': period_total['fee_amount__sum'],
            'total_operations': period_total['total__sum'],
            'clients': clients,
            'start_date': start_date,
            'end_date': end_date,
            'first': all_operations.first(),
            'last': all_operations.last(),
            'operations': operations,
            'client': client,
            'empty': empty,
        })

    return render(request, "manager/reports.html", {
        'clients': clients,
        'first': all_operations.first(),
        'last': all_operations.last()
    })
