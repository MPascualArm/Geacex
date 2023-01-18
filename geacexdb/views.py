from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from forms import *
from geacexdb.utils import *
import json

## Página de inicio ##

def index(request):

    return render(request, 'index.html')

## Cambio de contraseña de usuario ##

@login_required
def cambioPassword(request):
    
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) 
            messages.success(request, CONTRASENA_CAMBIO_OK)
            if(esCentro(request.user)):
                return redirect("centrologin")
            elif(esTutor(request.user)):
                return redirect("tutorlogin")
            else:
                return redirect("proveedorlogin")    
    else:
        form = PasswordForm(request.user)
    context = {
        'form': form
    }
    return render(request, "cambioContraseña.html", context)

## Login de centros educativos ##    

def centroLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and esCentro(user):
            login(request, user)
            # Login correcto.
            return redirect('grupos')
        else:
            # Login incorrecto.
            messages.error(request, LOGIN_ERROR)
            return redirect('.')
    else:    
        context = {
            'form': CentroLoginForm()
        }
        return render(request, 'centros/centroLogin.html', context)

## Registro de centros educativos ##        

def centroRegistro(request):

    if request.method == 'POST':
        form = CentroRegistroForm(request.POST)
        if form.is_valid():
            centro = CentroRegistroForm.save(form)
            messages.success(request, REGISTRO_OK)
            return redirect('centrologin') #Form valido, registro correcto
        else:
            messages.error(request, REGISTRO_ERROR)
            return redirect('.')
    else:
        context = {
            'form': CentroRegistroForm()
        }
        return render(request, 'centros/centroRegistro.html', context)

## Logout de centros ##        

def centroLogout(request):
    
    logout(request)
    messages.success(request, LOGOUT_OK)
    return redirect('centrologin')

## Consultar información de centro educativo ##

@login_required(login_url='/centros/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def infoCentro(request):

    usuario = request.user
    codigo_centro = getCodigo(usuario)
    if request.method == 'POST':
        form = CentroActForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, ACT_INFO_OK)
        return redirect('infocentro')
    else:
        context = {
            'codigo_centro': codigo_centro,
            'form': CentroActForm(instance=usuario)
        }
        return render(request, 'centros/infoCuenta.html', context)

## Crear calendario de actividades del centro educativo ##

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def crearCalendario(request):
    
    if request.method == 'POST':
        form = CalendarioForm(request.POST)
        if form.is_valid():
            calendario = form.save(commit=False)
            calendario.centro = Centro.objects.get(usuario=request.user)
            calendario.plazo_inscripcion = True
            calendario.save()
            messages.success(request, CALENDARIO_OK)
            return redirect('calendarios')

    else:
        context = {
            'form': CalendarioForm()
        }
        return render(request, 'centros/crearCalendario.html', context)

## Listado de calendarios del centro educativo ##        

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def calendarios(request):
    
    context = {
            'calendarios': Calendario.objects.filter(centro=Centro.objects.get(usuario=request.user)),
        }
    return render(request, 'centros/calendarios.html', context)

## Borrar un calendario ##

@login_required(login_url='/centros/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def borrarCalendario(request, id):
    calendario = get_object_or_404(Calendario, id=id)
    calendario.delete()
    messages.success(request, CALENDARIO_ELIMINADO)
    return redirect('calendarios')

## Actualizar un calendario ##

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def actualizarCalendario(request, id):

    calendario = Calendario.objects.get(id=id)
    if request.method == 'POST':
        form = CalendarioForm(request.POST, instance=calendario)
        if form.is_valid():
            form.save()
            messages.success(request, CALENDARIO_ACT_OK)
            return redirect('calendarios')
    else:
        context = {
            'form': CalendarioForm(instance=calendario)
        }
        return render(request, 'centros/actualizarCalendario.html', context)       

## Crear grupo de actividad en centro educativo ##  

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def crearGrupo(request):
    
    centro = Centro.objects.get(usuario=request.user)
    if request.method == 'POST':
        form = GrupoForm(None, request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.centro = centro
            grupo.save()
            form.save_m2m()
            messages.success(request, GRUPO_OK)
            return redirect('grupos')

    else:
        context = {
            'form': GrupoForm(usuario=centro),
        }
        return render(request, 'centros/crearGrupo.html', context)

## Borrar un grupo ##

@login_required(login_url='/centros/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def borrarGrupo(request, id):
    grupo = get_object_or_404(Grupo, id=id)
    grupo.delete()
    messages.success(request, GRUPO_ELIMINADO)
    return redirect('grupos')

## Actualizar un grupo ##

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def actualizarGrupo(request, id):

    grupo = Grupo.objects.get(id=id)
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, GRUPO_ACT_OK)
            return redirect('grupos')
    else:
        context = {
            'form': GrupoForm(instance=grupo)
        }
        return render(request, 'centros/actualizarGrupo.html', context)

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def alumnosGrupo(request, id):
    
    grupo = Grupo.objects.get(id=id)
    context = {
            'grupo': grupo,
            'alumnos': Alumno.objects.filter(grupo=grupo),
        }
    return render(request, 'centros/alumnosGrupo.html', context)



## Listado de grupos del centro educativo ##   

@login_required(login_url='/centros/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esCentro, login_url='/centros/login/')  # type: ignore
def grupos(request):
    
    context = {
            'grupos': Grupo.objects.filter(centro=Centro.objects.get(usuario=request.user)),
        }
    return render(request, 'centros/grupos.html', context)

## Login de tutores ##

def tutorLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and esTutor(user):
            login(request, user)
            # Login correcto.
            return redirect('alumnos')
        else:
            # Login incorrecto.
            messages.error(request, LOGIN_ERROR)
            return redirect('.')
    else:    
        context = {
            'form': TutorLoginForm()
        }
        return render(request, 'tutores/tutorLogin.html', context)

## Registro de tutores ##        

def tutorRegistro(request):

    if request.method == 'POST':
        centro = checkCodigo(request.POST['codigo'])
        if centro:
            form = TutorRegistroForm(request.POST)
            if form.is_valid():
              usuario = TutorRegistroForm.save(form, centro[0])
              messages.success(request, REGISTRO_OK)
              return redirect('tutorlogin') #Form valido, registro correcto
            else:
                messages.error(request, REGISTRO_ERROR)
                return redirect('.')
        else:
            messages.error(request, CODIGO_CENTRO_ERROR)
            return redirect('tutorregistro')
    else:
        context = {
            'form': TutorRegistroForm()
        }
        return render(request, 'tutores/tutorRegistro.html', context)

## Logout de tutores ##  
 
def tutorLogout(request):
    
    logout(request)
    messages.success(request, LOGOUT_OK)
    return redirect('tutorlogin')      

## Consultar información de tutor ##

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def infoTutor(request):

    usuario = request.user
    if request.method == 'POST':
        form = TutorActForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, ACT_INFO_OK)
        return redirect('infotutor')
    else:
        context = {
            'form': TutorActForm(instance=usuario)
        }
        return render(request, 'tutores/infoCuenta.html', context)

## Crear un nuevo alumno ##        

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def crearAlumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.tutor = Tutor.objects.get(usuario=request.user)
            actividad.save()
            form.save_m2m()
            messages.success(request, ALUMNO_OK)
            return redirect('alumnos')

    else:
        context = {
            'form': AlumnoForm()
        }
        return render(request, 'tutores/crearAlumno.html', context)

## Listado de alumnos de un tutor ##

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def alumnos(request):
    
    context = {
            'alumnos': Alumno.objects.filter(tutor=Tutor.objects.get(usuario=request.user)),
        }
    return render(request, 'tutores/alumnos.html', context)

## Borrar un alumno ##

@login_required(login_url='/tutores/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def borrarAlumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    alumno.delete()
    messages.success(request, ALUMNO_ELIMINADO)
    return redirect('alumnos')

## Actualizar un alumno ##

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def actualizarAlumno(request, id):

    alumno = Alumno.objects.get(id=id)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, ALUMNO_ACT_OK)
            return redirect('alumnos')
    else:
        context = {
            'form': AlumnoForm(instance=alumno)
        }
        return render(request, 'tutores/actualizarAlumno.html', context)    

## Inscribir alumno en grupo ##

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def inscribirAlumno(request, id):

    alumno = Alumno.objects.get(id=id)
    if request.method == 'POST':
        grupos_ids = json.loads(request.body)
        for grupo_id in grupos_ids.values():
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.alumnos.add(alumno)   
        data = {'exito':'exito',}
        return data
        
    else:
        gruposCentro = Grupo.objects.filter(centro=alumno.tutor.centro)
        actividadesCurso = Actividad.objects.filter(cursos=alumno.curso)
        grupos=[]
       
        for actividad in actividadesCurso:
          aux = gruposCentro.filter(actividad=actividad)
          for grupo in aux:
            if grupo.alumnos.count()<actividad.max_alumnos and alumno not in grupo.alumnos.all():
                grupos.append(grupo)  
       
        context = {
            'grupos': grupos,
            'alumno': alumno
        }

        return render(request, 'tutores/inscribirAlumno.html', context)

## Ver grupos de un alumno ##

@login_required(login_url='/tutores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esTutor, login_url='/tutores/login/')  # type: ignore
def gruposAlumno(request, id):

    alumno = Alumno.objects.get(id=id)
    if request.method == 'POST':
        grupos_ids = json.loads(request.body)
        for grupo_id in grupos_ids.values():
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.alumnos.remove(alumno) 
        data = {'exito':'exito',}
        return data   
    else:
        gruposAlumno=[]
        gruposCentro = Grupo.objects.filter(centro=alumno.tutor.centro)
        for grupo in gruposCentro:
            if alumno in grupo.alumnos.all():
                gruposAlumno.append(grupo)
        context = {
            'grupos': gruposAlumno,
            'alumno': alumno
        }

        return render(request, 'tutores/gruposAlumno.html', context)


## Login de proveedores ##

def proveedorLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and esProveedor(user):
            login(request, user)
            # Login correcto.
            return redirect('actividades')
        else:
            # Login incorrecto.
            messages.error(request, LOGIN_ERROR)
            return redirect('.')
    else:    
        context = {
            'form': ProveedorLoginForm()
        }
        return render(request, 'proveedores/proveLogin.html', context)

## Registro de proveedores ##

def proveedorRegistro(request):

    if request.method == 'POST':
        form = ProveedorRegistroForm(request.POST)
        if form.is_valid():
            usuario = ProveedorRegistroForm.save(form)
            messages.success(request, REGISTRO_OK)
            return redirect('proveedorlogin') #Form valido, registro correcto
        else:
            messages.error(request, REGISTRO_ERROR)
            return redirect('.')
    else:
        context = {
            'form': ProveedorRegistroForm()
        }
        return render(request, 'proveedores/proveRegistro.html', context)

## Logout de proveedores ##

def proveedorLogout(request):
    
    logout(request)
    messages.success(request, LOGOUT_OK)
    return redirect('proveedorlogin')

## Crear nueva actividad de un proveedor ##

@login_required(login_url='/proveedores/login', redirect_field_name=None)  # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def crearActividad(request):
    
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.proveedor = Proveedor.objects.get(usuario=request.user)
            actividad.save()
            form.save_m2m()
            messages.success(request, ACTIVIDAD_OK)
            return redirect('actividades')

    else:
        context = {
            'form': ActividadForm()
        }
        return render(request, 'proveedores/crearActividad.html', context)

## Listado de actividades de un proveedor ##

@login_required(login_url='/proveedores/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def actividades(request):
    
    context = {
            'actividades': Actividad.objects.filter(proveedor=Proveedor.objects.get(usuario=request.user)),
        }
    return render(request, 'proveedores/actividades.html', context)

## Borrar una actividad ##

@login_required(login_url='/proveedores/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def borrarActividad(request, id):
    act = get_object_or_404(Actividad, id=id)
    act.delete()
    messages.success(request, ACTIVIDAD_ELIMINADA)
    return redirect('actividades')

## Actualizar una actividad ##

@login_required(login_url='/proveedores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def actualizarActividad(request, id):

    act = Actividad.objects.get(id=id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            messages.success(request, ACTIVIDAD_ACT_OK)
            return redirect('actividades')
    else:
        context = {
            'form': ActividadForm(instance=act)
        }
        return render(request, 'proveedores/actualizarActividad.html', context)

## Consultar información de proveedor ##

@login_required(login_url='/proveedores/login/', redirect_field_name=None) # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def infoProveedor(request):

    usuario = request.user
    if request.method == 'POST':
        form = ProveedorActForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, ACT_INFO_OK)
        return redirect('infoproveedor')
    else:
        context = {
            'form': ProveedorActForm(instance=usuario)
        }
        return render(request, 'proveedores/infoCuenta.html', context)

## Grupos de una actividad del proveedor ##

@login_required(login_url='/proveedores/login/', redirect_field_name=None)  # type: ignore
@user_passes_test(esProveedor, login_url='/proveedores/login/')  # type: ignore
def gruposActividad(request, id):

    actividad = Actividad.objects.get(id=id)
    context = {
            'actividad': actividad,
            'grupos': Grupo.objects.filter(actividad=actividad)
        }
    return render(request, 'proveedores/gruposActividad.html', context)
   