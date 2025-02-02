from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User

class Trabajador(models.Model):
    id_t = models.AutoField(primary_key=True, verbose_name='Id de Trabajador')
    nombreCompleto_t= models.CharField(max_length=100, verbose_name='Nombre Trabajador')
    rut_t= models.IntegerField(verbose_name='Rut Trabajador')
    numeroTelefono_t= models.IntegerField(verbose_name='Numero Trabajador')
    email_t= models.CharField(max_length=100, unique=True, verbose_name='Correo Trabajador')
    contrasennia_t= models.CharField(max_length=25, verbose_name='Contraseña Trabajador')

    def __str__(self):
        return self.nombreCompleto_t

class Cliente(models.Model):
    id_c = models.AutoField(primary_key=True, verbose_name='Id de Cliente')
    nombreCompleto_c= models.CharField(max_length=100, verbose_name='Nombre Cliente')
    email_c= models.CharField(max_length=100, verbose_name='Correo Cliente')
    numeroTelefono_c= models.IntegerField(verbose_name='Numero Cliente')

    def __str__(self):
        return self.nombreCompleto_c
    
class Reserva(models.Model):
    id_r = models.AutoField(primary_key=True, verbose_name='Id Reserva')
    lugarTatuaje_r= models.CharField(max_length=50, verbose_name='Lugar Tatuaje')
    tamannio_r= models.CharField(max_length=20, null=True, blank=True, verbose_name='Tamaño Tatuaje')
    color_r= models.CharField(max_length=20, verbose_name='Color Tatuaje')
    hora_r = models.DateTimeField(verbose_name='Fecha y Hora')
    tatuador_r= models.ForeignKey(Trabajador, on_delete=models.CASCADE, verbose_name='Tatuador Reserva')
    cliente_r= models.ForeignKey(Cliente,on_delete=models.CASCADE,verbose_name='Cliente Reserva')
    descripcionTatuaje_r= models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripcion Tatuaje')
    referencia_r = models.ImageField(upload_to='img/img_cliente/', null=True, blank=True, verbose_name='Referencia Tatuaje')

    def __str__(self):
        return str(self.id_r)

class ClienteCuenta(models.Model):
    id_cc = models.AutoField(primary_key=True, verbose_name='Id Cliente')
    nombreClienteCuenta = models.CharField(max_length=100, verbose_name="Nombre Completo Cliente")
    emailClienteCuenta = models.CharField(max_length=100, unique=True, verbose_name='Correo Cliente')
    telefonoClienteCuenta = models.IntegerField(verbose_name="Teléfono Cliente")
    direccionClienteCuenta = models.CharField(max_length=100, verbose_name='Direccion Cliente')
    contrasenniaaClienteCuenta = models.CharField(max_length=25, verbose_name='Contraseña Cliente')  # Agregamos contraseña

    def __str__(self):
        return self.nombreClienteCuenta

    