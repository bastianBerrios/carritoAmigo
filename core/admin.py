from django.contrib import admin
from .models import Cliente,Trabajador,Reserva,ClienteCuenta

admin.site.register(Cliente)
admin.site.register(Trabajador)
admin.site.register(Reserva)
admin.site.register(ClienteCuenta)
# Register your models here.
