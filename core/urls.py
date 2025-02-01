from django.urls import path, include
from .views import (
    configuracion, index, calendario, confirmarHora, 
    contacto, crearUsuario, eliminarUsuario, job, login, 
    reservar, trabajo, about, eliminarUsuarioPorId, 
    modificarUsuario, obtener_detalles_trabajador, agregarHora,
    catalogo, agregarProducto, carrito, agregarCarrito, eliminarCarrito, limpiarCarrito
)

from django.conf import settings
from django.conf.urls.static import static

# from django.contrib import admin


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('calendario/', calendario, name='calendario'),
    path('contacto/', contacto, name='contacto'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'),
    path('eliminarUsuario/', eliminarUsuario, name='eliminarUsuario'),
    path('job/', job, name='job'),
    path('login/', login, name='login'),
    path('reservar/', reservar, name='reservar'),
    path('trabajo/', trabajo, name='trabajo'),
    path('configuracion/', configuracion, name='configuracion'),
    path('eliminarUsuario/<int:id_t>/', eliminarUsuarioPorId, name='eliminarUsuarioPorId'),
    path('modificarUsuario/', modificarUsuario, name='modificarUsuario'),
    path('obtener-detalles-trabajador/<int:id_t>/', obtener_detalles_trabajador, name='obtener_detalles_trabajador'),
    path('agregarHora/', agregarHora, name='agregarHora'),
    path('confirmarHora/', confirmarHora, name='confirmarHora'),

    # catalogo
    path('catalogo/', catalogo, name='catalogo'),  # Ahora haces referencia directamente a catalogo
    path('agregarProducto/', agregarProducto, name='agregarProducto'),
    
    path('carrito/', carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', agregarCarrito, name='agregarCarrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminarCarrito, name='eliminarCarrito'),
    path('carrito/limpiar/', limpiarCarrito, name='limpiarCarrito'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)