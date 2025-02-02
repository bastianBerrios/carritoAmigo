from django import forms
from django.forms import ModelForm
from .models import Trabajador, Cliente, Reserva, ClienteCuenta
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re
from datetime import date




class ReservaForm(forms.ModelForm):
    email_c = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electrónico',
            'id': 'email_c'
        }),
        label="Correo Electrónico"
    )

    nombreCompleto_c = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre Completo',
            'id': 'nombreCompleto_c'
        }),
        label="Nombre Completo"
    )

    numeroTelefono_c = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de Teléfono',
            'id': 'numeroTelefono_c'
        }),
        label="Número de Teléfono"
    )


    class Meta:
        model = Reserva
        fields = [
            'id_r', 
            'lugarTatuaje_r', 'tamannio_r', 'color_r', 'hora_r', 'tatuador_r', 
            'descripcionTatuaje_r', 'referencia_r'
        ]
        labels = {
            'id_r': 'ID de Reserva',
            'lugarTatuaje_r': 'Lugar del Tatuaje',
            'tamannio_r': 'Tamaño Aproximado',
            'color_r': '¿Color o Blanco y Negro?',
            'hora_r': 'Hora Preferida',
            'tatuador_r': 'Tatuador Preferido',
            'descripcionTatuaje_r': 'Descripción del Tatuaje',
            'referencia_r': 'Imagen de Referencia',
        }
        widgets = {
            'id_r': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese ID de Reserva',
                    'id': 'id_r'
                }
            ),
            'nombreCompleto_c': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre Completo',
                    'id': 'nombreCompleto_c'
                }
            ),
            'email_c': forms.EmailInput(  # Aquí fue el cambio
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico',
                    'id': 'email_c'
                }
            ),
            'numeroTelefono_c': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Numero de Teléfono',
                    'id': 'numeroTelefono_c'
                }
            ),
            'lugarTatuaje_r': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: Brazo derecho',
                    'id': 'lugar'
                }
            ),
            'tamannio_r': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: 10x10 cm',
                    'id': 'tamano'
                }
            ),
            'color_r': forms.Select(
                choices=[
                    ('Color', 'Color'), 
                    ('Blanco y Negro', 'Blanco y Negro')
                    ],
                attrs={
                    'class': 'form-select',
                    'id': 'color'
                }
            ),
            'hora_r': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DD HH:MM',
                    'id': 'hora'
                }
            ),

            'tatuador_r': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'tatuador'
                }
            ),  
            'descripcionTatuaje_r': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe tu diseño',
                    'id': 'descripcion',
                    'rows': 3
                }
            ),
            'referencia_r': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen',
                    'accept': 'image/*'
                }
            )
        }

    # constructor especial que empieza automaticamente
    # cuando se instancia la clase
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # llama al constructor de la base (modelform) para iniciar correctamente
        # el formulario con los argumentos dados (nombres)

        self.fields['tatuador_r'].queryset = Trabajador.objects.all()
        # se configura el campo [] para que use opciones (queryset) 
        # cargado desde el modelo trabajador
        # Trabajador.objects.all() recupera los registros del modelo trabajador
        # para mostrarlo como opciones desplegables

        self.fields['tatuador_r'].empty_label = "Seleccione un tatuador"
        # define la etiqueta como vacía en el menú, la cual aparece si no se 
        # ha seleccionado nada del menú

    def save(self, commit=True):
        email = self.cleaned_data.get('email_c')
        nombre_completo_c = self.cleaned_data.get('nombreCompleto_c')
        numeroTelefono_c = self.cleaned_data.get('numeroTelefono_c')
        # .cleaned_data contiene los datos del formulario listos para procesar

        cliente, created = Cliente.objects.get_or_create(
        # intenta encontrar un registro del modelo cliente con el correo
            # si no existe, crea un nuevo registro usando email_c y nombreCompleto_c
            # cliente creado o encontrado / booleano si se creó(t) o si existía(f)

            email_c=email,
            defaults={
                'nombreCompleto_c': nombre_completo_c,
                'numeroTelefono_c': numeroTelefono_c,
                }
        )

        # Si el cliente ya existe, actualizar el nombre completo y el número de teléfono si es necesario
        if not created:
            if cliente.nombreCompleto_c != nombre_completo_c or cliente.numeroTelefono_c != numeroTelefono_c:
                cliente.nombreCompleto_c = nombre_completo_c
                cliente.numeroTelefono_c = numeroTelefono_c
                cliente.save()

        # Asignar el cliente a la reserva
        self.instance.cliente = cliente

        # Guardar la reserva
        return super().save(commit)

class RegistroClienteCuentaForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = ClienteCuenta
        fields = ['nombreClienteCuenta', 'emailClienteCuenta', 'telefonoClienteCuenta', 'direccionClienteCuenta']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        # Crear un usuario asociado al ClienteCuenta
        cliente_cuenta = super().save(commit=False)

        # Crear el usuario con la contraseña
        user = User.objects.create_user(
            username=self.cleaned_data["emailClienteCuenta"],
            password=self.cleaned_data["password"]
        )

        # Asociar el usuario al ClienteCuenta
        cliente_cuenta.user = user

        if commit:
            cliente_cuenta.save()

        return cliente_cuenta



# parte de job.html
class ModificarTrabajadorForm(forms.ModelForm):
    repetir_contrasennia_t = forms.CharField(max_length=25, widget=forms.PasswordInput, label="Repetir Contraseña")

    class Meta:
        model = Trabajador
        fields = ['rut_t', 'numeroTelefono_t', 'email_t', 'contrasennia_t']  # No incluyas repetir_contrasennia_t en los campos del modelo

    def clean(self):
        cleaned_data = super().clean()
        contrasennia_t = cleaned_data.get('contrasennia_t')
        repetir_contrasennia_t = cleaned_data.get('repetir_contrasennia_t')

        if contrasennia_t != repetir_contrasennia_t:
            self.add_error('repetir_contrasennia_t', 'Las contraseñas no coinciden.')

        return cleaned_data

    
class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombreCompleto_t', 'rut_t', 'numeroTelefono_t', 'email_t', 'contrasennia_t']
        widgets = {
            'nombreCompleto_t': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_t': forms.NumberInput(attrs={'class': 'form-control rut-mask', 'maxlength': '12'}),  # Se mantiene como NumberInput
            'numeroTelefono_t': forms.TextInput(attrs={'class': 'form-control phone-mask', 'maxlength': '9'}),
            'email_t': forms.EmailInput(attrs={'class': 'form-control'}),
            'contrasennia_t': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_numeroTelefono_t(self):
        telefono = str(self.cleaned_data.get('numeroTelefono_t'))  # Convertir el número a cadena
        return telefono.replace(' ', '')  # Almacenar sin espacios