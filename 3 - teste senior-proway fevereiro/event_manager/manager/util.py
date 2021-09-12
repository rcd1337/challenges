from django.db.models import Q
from .models import Event_room, Coffee_space, Attendee


def count_max_attendees():
    rooms = Event_room.objects.all().order_by('capacity')
    smallest_room = Event_room.objects.all().order_by('capacity').first()
    largest_room = Event_room.objects.all().order_by('capacity').last()
    additional_attendees = 0
    for room in rooms:
        if room.capacity > smallest_room.capacity and room.capacity < largest_room:
            additional_attendees = additional_attendees + 1
    smallest_room_capacity = int(smallest_room.capacity)
    number_of_rooms = rooms.count()
    max_attendees = smallest_room_capacity * number_of_rooms + additional_attendees
    
    return max_attendees


def find_emptier_room():
    rooms = Event_room.objects.all()
    emptier_room = None
    index = 0
    for i in range(len(rooms)):
        if rooms[i].room1_assigneds.count() < rooms[index].room1_assigneds.count():
            index = i
        emptier_room = rooms[index]

    return emptier_room


def find_second_room(available_rooms):
    emptier_room = None
    index = 0
    for i in range(len(available_rooms)):
        if available_rooms[i].room2_assigneds.count() < available_rooms[index].room2_assigneds.count():
            index = i
        emptier_room = available_rooms[index]
    
    return emptier_room


def define_coffee_space(current_attendees):
    assigned_space = Coffee_space.objects.all()
    if current_attendees % 2 != 0:
        assigned_space = assigned_space.first()
    else:
        assigned_space = assigned_space.last()

    return assigned_space


def define_room_2():
    current_attendees = Attendee.objects.all().count()
    if current_attendees % 2 != 0:
        emptier_room = find_emptier_room()
        smallest_room = Event_room.objects.all().order_by('capacity').first()
        room_capacity = int(smallest_room.capacity) + 1
        if int(emptier_room.capacity) == int(smallest_room.capacity):
            room_capacity = int(smallest_room.capacity)
        occupancy = emptier_room.room2_assigneds.count()
        if occupancy < room_capacity:
            defined_room = emptier_room
        else:
            available_rooms = Event_room.objects.exclude(name=emptier_room.name)
            defined_room = find_second_room(available_rooms)
            if not defined_room.room2_assigneds.count() < int(smallest_room.capacity):
                available_rooms = Event_room.objects.exclude(Q(name=emptier_room.name) | Q(name=defined_room.name))
                defined_room = find_second_room(available_rooms)
    else:
        emptier_room = find_emptier_room()
        available_rooms = Event_room.objects.exclude(name=emptier_room.name)
        defined_room = find_second_room(available_rooms)
        if not defined_room.capacity > defined_room.room2_assigneds.count():
            defined_room = find_second_room(Event_room.objects.all())
        if not emptier_room.room1_assigneds.count() < int(emptier_room.capacity):
            defined_room = find_second_room(Event_room.objects.all())

    return defined_room


    