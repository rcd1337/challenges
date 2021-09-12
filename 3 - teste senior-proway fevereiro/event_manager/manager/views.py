from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Event_room, Coffee_space, Attendee
from .util import count_max_attendees, define_coffee_space, define_room_2, find_emptier_room, find_second_room


def index(request):
    return render(request, "manager/index.html")


def cadastro(request):
    if len(Event_room.objects.all()) < 1:
        return HttpResponseRedirect(reverse("pre_cadastro_sala"))
    
    if len(Coffee_space.objects.all()) < 2:
        return HttpResponseRedirect(reverse("cadastro_cafe"))

    if request.method == "POST":
        name = request.POST['name']
        last_name = request.POST['last_name']
        
        if not name or not last_name:
            return render(request, "manager/cadastro.html", {
                "message": f'Cadastro não efetuado. NOME ou SOBRENOME inválidos.'
            })

        current_attendees = Attendee.objects.all().count()

        if count_max_attendees() > current_attendees:
           
            event_room_1 = find_emptier_room()

            event_room_2 = define_room_2()

            assigned_space = define_coffee_space(current_attendees)

            new_entry = Attendee(name=name, last_name=last_name, event_room_1=event_room_1, event_room_2=event_room_2, coffee_space=assigned_space)
            new_entry.save()
        else:
            return render(request, "manager/cadastro.html", {
                "message": f'Cadastro não efetuado. Capacidade máxima de participantes cadastrados foi atingida.'
            })

        return render(request, "manager/cadastro.html", {
            "message": f'Participante "{name} {last_name}" foi cadastrado com sucesso.'
        })

    return render(request, "manager/cadastro.html")

def pre_cadastro_sala(request):
    if len(Event_room.objects.all()) > 0:
        return HttpResponseRedirect(reverse("cadastro_sala"))

    return render(request, "manager/pre_cadastro_sala.html")


def cadastro_sala(request):
    forms_quantity = 0
    number_list = []
    
    if request.method == "POST":
        rooms_quantity = int(request.POST['quantity'])
        for i in range(rooms_quantity):
            name = request.POST[f'name{i}']
            capacity = request.POST[f'capacity{i}']
            if not name or not capacity:
                abort_entries = Event_room.objects.all().delete()
                abort_entries.save()
                return render(request, "manager/pre_cadastro_sala.html", {
                    "message": f'Cadastro não efetuado. NOME ou LOTAÇÃO MÁXIMA inválidos.',
                })
            new_entry = Event_room(name=name, capacity=capacity)
            new_entry.save()
        return HttpResponseRedirect(reverse("cadastro"))

    if request.method == "GET":
        rooms = Event_room.objects.all()
        if len(rooms) > 0:
            rooms_list = []
            for room in range(len(rooms)):
                rooms_list.append(f'Sala "{rooms[room].name}". Capacidade: {rooms[room].capacity}')
            return render(request, "manager/cadastro_sala.html", {
                "rooms": rooms_list
            })
        
        try:
            forms_quantity = int(request.GET.get('quantity', ''))
        except ValueError:
            return render(request, "manager/pre_cadastro_sala.html", {
            "message": "Número de salas inválido."
            })
        
        if forms_quantity < 1:
            return render(request, "manager/pre_cadastro_sala.html", {
            "message": "Número de salas deve ser um maior que 0."
            })
       
        for i in range(forms_quantity):
            number_list.append(i)

    return render(request, "manager/cadastro_sala.html", {
        "number_list": number_list,
        "quantity": forms_quantity
    })


def cadastro_cafe(request):
    spaces = Coffee_space.objects.all()
    
    if len(spaces) > 0:
        spaces_list = []
        for space in range(len(spaces)):
            spaces_list.append(f'Espaço "{spaces[space].name}". Capacidade: {spaces[space].capacity}')
        
        return render(request, "manager/cadastro_cafe.html", {
            "spaces": spaces_list
        })
    
    if request.method == "POST":
        name1 = request.POST['name1']
        capacity1 = request.POST['capacity1']
        name2 = request.POST['name2']
        capacity2 = request.POST['capacity2']
        
        if not name1 or not capacity1 or not name2 or not capacity2:
            return render(request, "manager/cadastro_cafe.html", {
                "message": f'Cadastro não efetuado. NOME ou LOTAÇÃO MÁXIMA inválidos.'
            })

        spaces.delete()
        new_entry1 = Coffee_space(name=name1, capacity=capacity1)
        new_entry2 = Coffee_space(name=name2, capacity=capacity2)
        new_entry1.save()
        new_entry2.save()

        return HttpResponseRedirect(reverse("cadastro"))

    return render(request, "manager/cadastro_cafe.html")


def consulta(request):
    if request.method == "POST":
        name = request.POST['name']
        last_name = request.POST['last_name']

        query = Attendee.objects.filter(name=name, last_name=last_name)

        if not name or not last_name or len(query) < 1:
            return render(request, "manager/consulta.html", {
                "message": f'Participante não cadastrado ou dados inválidos.'
            })

        return render(request, "manager/consulta.html", {
            "attendees": query
        })
    
    return render(request, "manager/consulta.html")


def consulta_sala(request):
    rooms = Event_room.objects.all()
    rooms_list = []
    for room in range(len(rooms)):
        rooms_list.append(rooms[room])

    if request.method == "POST":
        name = request.POST['name']
        
        attendees_room_1 = Attendee.objects.filter(event_room_1=Event_room.objects.get(name=name))
        attendees_room_2 = Attendee.objects.filter(event_room_2=Event_room.objects.get(name=name))
        room = Event_room.objects.get(name=name)

        if (attendees_room_1.count() + attendees_room_2.count()) < 1:
            return render(request, "manager/consulta_sala.html", {
            "message": "Não há participantes cadastrados nesta sala.",
            "room_name": name,
            "rooms": rooms_list
        })

        return render(request, "manager/consulta_sala.html", {
            "attendees_1": attendees_room_1,
            "attendees_2": attendees_room_2,
            "room_name": name,
            "rooms": rooms_list,
            "capacity": room.capacity,
            "occupancy_1": attendees_room_1.count(),
            "occupancy_2": attendees_room_2.count()
        })
    
    return render(request, "manager/consulta_sala.html", {
        "rooms": rooms_list
    })


def consulta_cafe(request):
    spaces = Coffee_space.objects.all()
    spaces_list = []
    for space in range(len(spaces)):
        spaces_list.append(spaces[space])

    if request.method == "POST":
        name = request.POST['name']

        query = Attendee.objects.filter(coffee_space=Coffee_space.objects.get(name=name))

        if query.count() < 1:
            return render(request, "manager/consulta_sala.html", {
            "message": "Não há participantes cadastrados neste espaço.",
            "space_name": name,
            "spaces": spaces_list
            })
        
        capacity = query[0].coffee_space.capacity
        occupancy = query.count()

        return render(request, "manager/consulta_cafe.html", {
            "attendees": query,
            "space_name": name,
            "spaces": spaces_list,
            "capacity": capacity,
            "occupancy": occupancy
        })
    
    return render(request, "manager/consulta_cafe.html", {
        "spaces": spaces_list
    })

