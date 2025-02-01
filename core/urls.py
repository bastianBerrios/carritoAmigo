from django.urls import path
from .views import (
    index,about,calendario,confirmarHora,contacto,crearUsuario,eliminarUsuario,job,
    login,modificarUsuario,reservar,trabajo, registro_cliente_cuenta, logout, configuracion,
    agregarHora,eliminarUsuarioPorId,obtener_detalles_trabajador
) 

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('calendario/', calendario, name='calendario'), 
    path('confirmarHora/', confirmarHora, name='confirmarHora'),
    path('contacto/', contacto, name='contacto'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'), 
    path('eliminarUsuario/', eliminarUsuario, name='eliminarUsuario'), 
    path('job/', job, name='job'),
    path('login/', login, name='login'),
    path('modificarUsuario/', modificarUsuario, name='modificarUsuario'),
    path('reservar/', reservar, name='reservar'),
    path('trabajo/', trabajo, name='trabajo'),
    path('registro/', registro_cliente_cuenta, name='registro_cliente_cuenta'),
    path('logout/', logout, name='logout'),
    path('configuracion/', configuracion, name='configuracion'),
    path('eliminarUsuario/<int:id_t>/', eliminarUsuarioPorId, name='eliminarUsuarioPorId'),
    path('obtener-detalles-trabajador/<int:id_t>/', obtener_detalles_trabajador, name='obtener_detalles_trabajador'),
    path('agregarHora/', agregarHora, name='agregarHora'),
]


# IMPORTANTE: Añadir a los html {%csf_token%}
# se utiliza para proteger mi pagina de posibles ataques (inf. privada de usuarios)