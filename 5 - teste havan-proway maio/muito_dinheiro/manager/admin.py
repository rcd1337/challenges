from django.contrib import admin

# Register your models here.
from .models import Client, Currency, Operation

admin.site.register(Client)
admin.site.register(Currency)
admin.site.register(Operation)