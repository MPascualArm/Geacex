"""geacex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from geacexdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cambio_password', views.cambioPassword, name='cambiopassword'),
    path('centros/crear_calendario', views.crearCalendario, name='crearcalendario'),
    path('centros/calendarios', views.calendarios, name='calendarios'),
    path('centros/borrar_cal/<str:id>/', views.borrarCalendario, name='borrarcalendario'),
    path('centros/actualizar_cal/<str:id>/', views.actualizarCalendario, name='actualizarcalendario'),
    path('centros/crear_grupo', views.crearGrupo, name='creargrupo'),
    path('centros/grupos', views.grupos, name='grupos'),
    path('centros/alumnos_grupo/<str:id>/', views.alumnosGrupo, name='alumnosgrupo'),
    path('centros/borrar_grupo/<str:id>/', views.borrarGrupo, name='borrargrupo'),
    path('centros/actualizar_grupo/<str:id>/', views.actualizarGrupo, name='actualizargrupo'),
    path('centros/login/', views.centroLogin, name='centrologin'),
    path('centros/logout', views.centroLogout, name='centrologout'),
    path('centros/registro/', views.centroRegistro, name='centroregistro'),  # type: ignore
    path('centros/info/', views.infoCentro, name='infocentro'),
    path('tutores/login/', views.tutorLogin, name='tutorlogin'),
    path('tutores/logout', views.tutorLogout, name='tutorlogout'),
    path('tutores/registro/', views.tutorRegistro, name='tutorregistro'),  # type: ignore
    path('tutores/crear_alumno/', views.crearAlumno, name='crearalumno'),
    path('tutores/alumnos/', views.alumnos, name='alumnos'),
    path('tutores/borrar_alumno/<str:id>/', views.borrarAlumno, name='borraralumno'),
    path('tutores/actualizar_alumno/<str:id>/', views.actualizarAlumno, name='actualizaralumno'),
    path('tutores/inscribir_alumno/<str:id>/', views.inscribirAlumno, name='inscribiralumno'),
    path('tutores/grupos_alumno/<str:id>/', views.gruposAlumno, name='gruposalumno'),
    path('tutores/info/', views.infoTutor, name='infotutor'),
    path('proveedores/login/', views.proveedorLogin, name='proveedorlogin'),
    path('proveedores/logout/', views.proveedorLogout, name='proveedorlogout'),
    path('proveedores/registro/', views.proveedorRegistro, name='proveedorregistro'),    # type: ignore
    path('proveedores/crear_actividad/', views.crearActividad, name='crearactividad'),  
    path('proveedores/actividades/', views.actividades, name='actividades'),
    path('proveedores/borrar_act/<str:id>/', views.borrarActividad, name='borraractividad'),
    path('proveedores/actualizar_act/<str:id>/', views.actualizarActividad, name='actualizaractividad'),
    path('proveedores/grupos_act/<str:id>/', views.gruposActividad, name='gruposactividad'),
    path('proveedores/info/', views.infoProveedor, name='infoproveedor'),
]
