from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente,Trabajador,Reserva, ClienteCuenta
from .forms import ReservaForm, ModificarTrabajadorForm, CrearUsuarioForm,RegistroClienteCuentaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from django.http import HttpResponseRedirect


def configuracion(request):
    return render(request, 'configuracion.html')

def agregarHora(request):
    return render(request, 'agregarHora.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def calendario(request):
    return render(request, 'calendario.html')

def confirmarHora(request):
    return render(request, 'confirmarHora.html')

def contacto(request):
    return render(request, 'contacto.html')

def crearUsuario(request):
    return render(request, 'crearUsuario.html')

def eliminarUsuario(request):
    return render(request, 'eliminarUsuario.html')

def job(request):
    return render(request, 'job.html')

def login(request):
    return render(request, 'login.html')

def modificarUsuario(request):
    return render(request, 'modificarUsuario.html')



def trabajo(request):
    return render(request, 'trabajo.html')

def reservar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES)  # Agregar request.FILES para manejar archivos
        if form.is_valid():
            # Obtener el cliente del formulario
            email = form.cleaned_data['email_c']
            nombre_completo_c = form.cleaned_data['nombreCompleto_c']
            numeroTelefono_c = form.cleaned_data['numeroTelefono_c']

            # Crear o obtener el cliente
            cliente, created = Cliente.objects.get_or_create(
                email_c=email,
                defaults={'nombreCompleto_c': nombre_completo_c, 'numeroTelefono_c': numeroTelefono_c},
            )

            # Si el cliente ya existe, actualizar los datos si es necesario
            if not created:
                if cliente.nombreCompleto_c != nombre_completo_c or cliente.numeroTelefono_c != numeroTelefono_c:
                    cliente.nombreCompleto_c = nombre_completo_c
                    cliente.numeroTelefono_c = numeroTelefono_c
                    cliente.save()

            # Asignar el cliente a la reserva
            reserva = form.save(commit=False)
            reserva.cliente_r = cliente  # Asignar el cliente
            reserva.save()  # Guardar la reserva

            # Muestra un mensaje de éxito
            messages.success(request, '¡Reserva realizada con éxito!')

            # Renderiza la página con el formulario vacío
            return redirect('index') # Cambiar por el nombre de la vista de redirección
        else:
            # Si el formulario no es válido, muestra un mensaje de error
            messages.error(request, 'Hubo un error con la reserva. Por favor, revisa los datos.')
            return render(request, 'reservar.html', {'form': form})
    else:
        form = ReservaForm()

    return render(request, 'reservar.html', {'form': form})

def registro_cliente_cuenta(request):
    if request.method == "POST":
        form = RegistroClienteCuentaForm(request.POST)
        if form.is_valid():
            # Guardar el cliente cuenta y el usuario asociado
            form.save()
            messages.success(request, "Tu cuenta ha sido creada exitosamente. ¡Ahora puedes iniciar sesión!")
            return redirect('login')  # Redirigir a la página de login
        else:
            # Si el formulario no es válido, mostramos los errores
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroClienteCuentaForm()
    
    return render(request, 'registro_cliente_cuenta.html', {'form': form})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Verificar si es un Trabajador
        trabajador = Trabajador.objects.filter(email_t=email, contrasennia_t=password).first()
        if trabajador:
            request.session['usuario_id'] = trabajador.id_t
            request.session['tipo_usuario'] = 'trabajador'
            messages.success(request, "¡Bienvenido, Trabajador!")
            return redirect('calendario')  # Redirigir a la página de trabajadores
        
        # Verificar si es un ClienteCuenta
        cliente = ClienteCuenta.objects.filter(emailClienteCuenta=email, contraseñaClienteCuenta=password).first()
        if cliente:
            request.session['usuario_id'] = cliente.id_cc
            request.session['tipo_usuario'] = 'cliente'
            messages.success(request, "¡Bienvenido, Cliente!")
            return redirect('index')  # Redirigir a la página principal

        messages.error(request, "Credenciales incorrectas")
    
    return render(request, "login.html")

def logout(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión")
    return redirect('index')



#parte de Admin (job.html)
def listar_trabajadores(request):
    trabajadores = Trabajador.objects.all()  # Obtiene todos los trabajadores
    return render(request, 'eliminarUsuario.html', {'trabajadores': trabajadores})

def eliminarUsuario(request):
    if request.method == 'GET':
        # Obtener la lista de trabajadores desde la base de datos
        trabajadores = Trabajador.objects.all()
        return render(request, 'eliminarUsuario.html', {'trabajadores': trabajadores})

@csrf_exempt
def eliminarUsuarioPorId(request, id_t):
    if request.method == 'DELETE':
        try:
            trabajador = Trabajador.objects.get(id_t=id_t)
            trabajador.delete()
            return JsonResponse({'message': 'Trabajador eliminado correctamente.'}, status=200)
        except Trabajador.DoesNotExist:
            return JsonResponse({'error': 'Trabajador no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def modificarUsuario(request):
    if request.method == 'POST':
        trabajador_id = request.POST.get('trabajador_id')  # Obtener el ID del trabajador
        trabajador = Trabajador.objects.get(id_t=trabajador_id)  # Usar 'id_t' en lugar de 'id'

        # Actualizar los campos del trabajador
        trabajador.nombreCompleto_t = request.POST.get('nombre')
        trabajador.email_t = request.POST.get('correo')
        trabajador.numeroTelefono_t = request.POST.get('telefono')
        trabajador.contrasennia_t = request.POST.get('contraseña')  # Asegúrate de que los nombres de los campos coincidan con tu modelo

        trabajador.save()  # Guardar los cambios

        # Redirigir con el parámetro 'success=true' en la URL
        return HttpResponseRedirect(request.path + '?success=true')

    trabajadores = Trabajador.objects.all()
    return render(request, 'modificarUsuario.html', {'trabajadores': trabajadores})


def obtener_detalles_trabajador(request, id_t):
    trabajador = Trabajador.objects.get(id=id_t)
    data = {
        'nombre': trabajador.nombre,
        'correo': trabajador.correo,
        'telefono': trabajador.telefono,
        'contraseña': trabajador.contraseña,
    }
    return JsonResponse(data)


def obtener_detalles_trabajador(request, id_t):
    # Buscar al trabajador por ID
    try:
        trabajador = Trabajador.objects.get(id_t=id_t)
        data = {
            'nombre': trabajador.nombreCompleto_t,
            'correo': trabajador.email_t,
            'telefono': trabajador.numeroTelefono_t,
            'contraseña': trabajador.contrasennia_t,
        }
        return JsonResponse(data)
    except Trabajador.DoesNotExist:
        return JsonResponse({'error': 'Trabajador no encontrado'}, status=404)







def crearUsuario(request):
    form = CrearUsuarioForm()  # Inicializa el formulario *aquí*, antes del if

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)  # Reasigna el formulario *solo* si es POST
        if form.is_valid():
            rut = form.cleaned_data['rut_t']
            email = form.cleaned_data['email_t']

            if Trabajador.objects.filter(rut_t=rut).exists():
                messages.error(request, 'Ya existe un trabajador con este RUT.')
            elif Trabajador.objects.filter(email_t=email).exists():
                messages.error(request, 'Ya existe un trabajador con este correo.')
            else:
                form.save()
                messages.success(request, 'Trabajador registrado exitosamente.')
                return redirect('crearUsuario')  # ¡REDIRECCIÓN AQUÍ!
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{form[field].label}: {error}")
            # Si hay errores en el formulario, *también* redirige para mostrar los mensajes.
            return redirect('crearUsuario')

    return render(request, 'crearUsuario.html', {'form': form})  



