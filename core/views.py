from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Trabajador, Reserva, Producto
from django.contrib import messages
from .forms import ReservaForm,ModificarTrabajadorForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from django.contrib.auth import authenticate, login , logout


from .forms import ProductoForm

@login_required
# Vistas básicas
def index(request):
    return render(request, 'index.html')

def agregarHora(request):
    return render (request, 'agregarHora')

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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Correo o contraseña incorrectos')
            return render(request, 'login.html')

    return render(request, 'login.html')

def trabajo(request):
    return render(request, 'trabajo.html')

def configuracion(request):
    return render(request, 'configuracion.html')

# Vista de reservas
def reservar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES)  # Manejo de archivos
        if form.is_valid():
            # Obtener los datos del cliente desde el formulario
            email = form.cleaned_data['email_c']
            nombre_completo_c = form.cleaned_data['nombreCompleto_c']
            numeroTelefono_c = form.cleaned_data['numeroTelefono_c']

            # Crear o actualizar cliente
            cliente, created = Cliente.objects.get_or_create(
                email_c=email,
                defaults={
                    'nombreCompleto_c': nombre_completo_c,
                    'numeroTelefono_c': numeroTelefono_c
                }
            )

            # Actualizar datos del cliente si ya existe
            if not created:
                if cliente.nombreCompleto_c != nombre_completo_c or cliente.numeroTelefono_c != numeroTelefono_c:
                    cliente.nombreCompleto_c = nombre_completo_c
                    cliente.numeroTelefono_c = numeroTelefono_c
                    cliente.save()

            # Asignar el cliente a la reserva y guardar
            reserva = form.save(commit=False)
            reserva.cliente_r = cliente
            reserva.save()

            # Mostrar mensaje de éxito y redirigir
            messages.success(request, '¡Reserva realizada con éxito!')
            return redirect('index')  # Cambia por el nombre de la vista de redirección
        else:
            # Manejo de errores del formulario
            messages.error(request, 'Hubo un error con la reserva. Por favor, revisa los datos.')
            return render(request, 'reservar.html', {'form': form})
    else:
        form = ReservaForm()

    return render(request, 'reservar.html', {'form': form})

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


#de modificarUsuarios.html(de trabajadores parte admin)

def modificarUsuario(request):
    # Obtener todos los trabajadores
    trabajadores = Trabajador.objects.all()

    if request.method == 'POST':
        # Aquí es donde manejarás la lógica para actualizar un trabajador
        trabajador_id = request.POST.get('trabajador_id')
        trabajador = Trabajador.objects.get(id=trabajador_id)
        
        # Actualiza los campos según el formulario enviado (ej. nombre, email, etc.)
        trabajador.nombre = request.POST.get('nombre')
        trabajador.correo = request.POST.get('correo')
        trabajador.telefono = request.POST.get('telefono')
        trabajador.contraseña = request.POST.get('contraseña')
        trabajador.save()

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

# catalogo
# mostra el fakin catalogo
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'core/catalogo.html', {'productos':productos})

# agregar el fakin producto
def agregarProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # guarda el producto
            messages.success(request, '¡Producto Agregado!')
            return redirect('catalogo')  # manda al catalogo al agregar
        else:
            messages.success(request, '¡Error al Agregar! Revisa los datos...')
    else:
        form = ProductoForm()
    return render(request, 'agregarProducto.html', {'form': form})

# carrito de compras
def agregarCarrito(request, producto_id):
    try:
        producto = Producto.objects.get(id_p=producto_id)  # Asegúrate de que el campo se llame id_p
        carrito = request.session.get('carrito', {})
        if producto_id in carrito:
            carrito[producto_id] += 1
        else:
            carrito[producto_id] = 1
        request.session['carrito'] = carrito
        return redirect('carrito')  # Redirige a la página del carrito
    except Producto.DoesNotExist:
        return redirect('producto_no_encontrado')  # Manejo de error si el producto no existe

def eliminarCarrito(request, id_p):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id_p=id_p)
    carrito.eliminar(producto)
    messages.success(request, f'{producto.nombre_p} eliminado del carrito.')
    return redirect('carrito')

def limpiarCarrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    messages.info(request, 'Carrito limpiado con éxito.')
    return redirect('carrito')

def carrito(request):
    return render(request, 'core/carrito.html', {
        'carrito': request.session.get('carrito', {})
    })