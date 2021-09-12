from django.contrib import admin

from .models import Event_room, Coffee_space, Attendee

# Register your models here.
admin.site.register(Event_room)
admin.site.register(Coffee_space)
admin.site.register(Attendee)
