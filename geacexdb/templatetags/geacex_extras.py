from django import template

register = template.Library()

## Comprobar si el usuario es un centro ##
@register.filter
def esCentro(usuario):
    return usuario.es_centro

## Comprobar si el usuario es un tutor ##
@register.filter
def esTutor(usuario):
    return usuario.es_tutor

## Comprobar si el usuario es un proveedor ##
@register.filter
def esProveedor(usuario):
    return usuario.es_proveedor
  