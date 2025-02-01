from django import forms
from django.forms import ModelForm
from .models import Trabajador, Cliente, Reserva, Producto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class ReservaForm(forms.ModelForm):
    # Campos adicionales para capturar los datos del cliente
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
            'lugarTatuaje_r', 'tamannio_r', 'color_r', 'hora_r', 'tatuador_r', 
            'descripcionTatuaje_r', 'referencia_r'
        ]
        labels = {
            'lugarTatuaje_r': 'Lugar del Tatuaje',
            'tamannio_r': 'Tamaño Aproximado',
            'color_r': '¿Color o Blanco y Negro?',
            'hora_r': 'Hora Preferida',
            'tatuador_r': 'Tatuador Preferido',
            'descripcionTatuaje_r': 'Descripción del Tatuaje',
            'referencia_r': 'Imagen de Referencia',
        }
        widgets = {
            'lugarTatuaje_r': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Brazo derecho',
                'id': 'lugar'
            }),
            'tamannio_r': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: 10x10 cm',
                'id': 'tamano'
            }),
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
            'tatuador_r': forms.Select(attrs={
                'class': 'form-control',
                'id': 'tatuador'
            }),
            'descripcionTatuaje_r': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe tu diseño',
                'id': 'descripcion',
                'rows': 3
            }),
            'referencia_r': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'imagen',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tatuador_r'].queryset = Trabajador.objects.all()
        self.fields['tatuador_r'].empty_label = "Seleccione un tatuador"

    def save(self, commit=True):
        email = self.cleaned_data.get('email_c')
        nombre_completo_c = self.cleaned_data.get('nombreCompleto_c')
        numeroTelefono_c = self.cleaned_data.get('numeroTelefono_c')

        # Crear o actualizar cliente
        cliente, created = Cliente.objects.get_or_create(
            email_c=email,
            defaults={
                'nombreCompleto_c': nombre_completo_c,
                'numeroTelefono_c': numeroTelefono_c,
            }
        )

        if not created:  # Si el cliente ya existe, actualizamos los datos si son diferentes
            if cliente.nombreCompleto_c != nombre_completo_c or cliente.numeroTelefono_c != numeroTelefono_c:
                cliente.nombreCompleto_c = nombre_completo_c
                cliente.numeroTelefono_c = numeroTelefono_c
                cliente.save()

        # Asignar el cliente a la reserva
        self.instance.cliente_r = cliente

        # Guardar la reserva
        return super().save(commit)



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

# formulario para agregar producto al catalogo | pip install django-crispy-forms
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_p', 'descripcion_p', 'precio_p', 'cantidad_p', 'imagen_p']  # Aquí los campos de tu modelo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Método POST para el formulario
        self.helper.layout = Layout(
            Row(
                Column('nombre_p', css_class='form-group col-md-6 mb-0'),  # 'nombre_p' en la primera columna
                Column('precio_p', css_class='form-group col-md-6 mb-0'),   # 'precio_p' en la segunda columna
                css_class='form-row'
            ),
            Row(
                Column('descripcion_p', css_class='form-group col-md-12 mb-0'),  # 'descripcion_p' en toda la fila
                css_class='form-row'
            ),
            Row(
                Column('cantidad_p', css_class='form-group col-md-6 mb-0'),  # 'cantidad_p' en la primera columna
                Column('imagen_p', css_class='form-group col-md-6 mb-0'),    # 'imagen_p' en la segunda columna
                css_class='form-row'
            ),
            Submit('submit', 'Guardar Producto', css_class='btn btn-success mt-3')  # Botón de submit
        )

class AgregarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_p', 'descripcion_p', 'precio_p', 'cantidad_p', 'imagen_p']
        widgets = {
            'descripcion_p': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(AgregarProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombre_p', css_class='form-group col-md-6 mb-0'),
                Column('precio_p', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'descripcion_p',
            Row(
                Column('cantidad_p', css_class='form-group col-md-6 mb-0'),
                Column('imagen_p', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Agregar Producto', css_class='btn btn-primary')
        )