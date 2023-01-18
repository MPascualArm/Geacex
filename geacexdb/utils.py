import random
import string
from django.core import serializers
from geacexdb.models import Centro

## Constantes para la aplicación ##

LOGIN_OK = "Login correcto"
LOGIN_ERROR = "Login incorrecto"
LOGOUT_OK = "Sesión cerrada con éxito"
CODIGO_CENTRO_ERROR = "El código de centro es incorrecto"
ACTIVIDAD_OK = "Actividad añadida con éxito"
ACTIVIDAD_ACT_OK = "Actividad actualizada con éxito"
ACTIVIDAD_ELIMINADA = "Actividad eliminada"
ACT_INFO_OK = "Información actualizada con éxito"
CONTRASENA_CAMBIO_OK = "La contraseña se ha cambiado con éxito"
ALUMNO_OK = "Alumno creado con éxito"
ALUMNO_ACT_OK = "Alumno actualizado con éxito"
ALUMNO_ELIMINADO = "Alumno eliminado"
CALENDARIO_OK = "Calendario creado con éxito"
CALENDARIO_ELIMINADO = "Calendario eliminado"
CALENDARIO_ACT_OK = "Calendario actualizado con éxito"
GRUPO_OK = "Grupo creado con éxito"
GRUPO_ELIMINADO = "Grupo eliminado"
GRUPO_ACT_OK = "Grupo actualizado con éxito"
ALUMNO_INSCRITO_OK = "El alumno ha sido inscrito con éxito"
ALUMNO_BAJA_OK = "El alumno se ha dado de baja del grupo con éxito"
REGISTRO_OK = "El usuario se ha registrado con éxito. Ya puede iniciar sesión"
REGISTRO_ERROR = "Hay errores en el formulario de registro"

## Generar código alfanumérico de 6 caracteres asociado al centro educativo ##
def setCodigo():
    conjunto = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(conjunto) for i in range(6))
    return codigo

## Obtener código del centro educativo ##

def getCodigo(usuario):
    centro = Centro.objects.get(usuario_id=usuario.id)
    return centro.codigo 
 
## Comprobar si un código está asociado a un centro educativo ##
def checkCodigo(codigo):
    return Centro.objects.filter(codigo=codigo)
    
## Comprobar si el usuario es un centro ##
def esCentro(usuario):
    return usuario.es_centro

## Comprobar si el usuario es un tutor ##
def esTutor(usuario):
    return usuario.es_tutor

## Comprobar si el usuario es un proveedor ##
def esProveedor(usuario):
    return usuario.es_proveedor
