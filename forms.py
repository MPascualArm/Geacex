from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm, TextInput
from localflavor.es.forms import ESIdentityCardNumberField as dniField, ESProvinceSelect
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.layout import Submit
from geacexdb.utils import setCodigo


from geacexdb.models import *
from django.db import transaction

## Formulario de registro de centro ##

class CentroRegistroForm(UserCreationForm):
    provincia = forms.CharField(widget=ESProvinceSelect)
    localidad = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['first_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))
    
    @transaction.atomic
    def save(self):
        usuario = super().save(commit=False)
        usuario.es_centro = True
        usuario.save()
        centro = Centro(usuario=usuario, provincia=self.cleaned_data['provincia'], localidad=self.cleaned_data['localidad'], codigo=setCodigo())
        centro.save()
        return centro

## Formulario de login de centro ##

class CentroLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de actualización de Centro ##        

class CentroActForm(UserChangeForm):
    
    password = None

    class Meta:
        model = Usuario
        fields = ['first_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de registro de tutor ##

class TutorRegistroForm(UserCreationForm):
    dni = dniField()
    codigo = forms.CharField(max_length=6, label="Código de centro. Código de 6 caracteres proporcionado por tu centro educativo")
    
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

    @transaction.atomic
    def save(self, centro):
        usuario = super().save(commit=False)
        usuario.es_tutor = True
        usuario.save()
        tutor = Tutor(usuario=usuario, dni=self.cleaned_data['dni'], centro=centro)
        tutor.save()
        return usuario

## Formulario de login de tutor ##

class TutorLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de actualización de tutor ##        

class TutorActForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))
        
## Formulario de registro de proveedor ##

class ProveedorRegistroForm(UserCreationForm):
    nif = dniField()

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['first_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

    @transaction.atomic
    def save(self):
        usuario = super().save(commit=False)
        usuario.es_proveedor = True
        usuario.save()
        proveedor = Proveedor(usuario=usuario, nif=self.cleaned_data['nif'])
        proveedor.save()
        return usuario

## Formulario de login de proveedor ##

class ProveedorLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de actualización de proveedor ##        

class ProveedorActForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ['first_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de actividad ##

class ActividadForm(ModelForm):
    
    class Meta:
        model = Actividad
        fields = ['nombre', 'min_alumnos', 'max_alumnos', 'precio', 'cursos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de alumno ##

class AlumnoForm(ModelForm):
    
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido1', 'apellido2', 'edad', 'curso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de calendario ##

class CalendarioForm(ModelForm):

    class Meta:
        model = Calendario
        fields = ['nombre', 'dia_inicio', 'dia_final', 'plazo_inscripcion']
        widgets = {
            'dia_inicio': TextInput(attrs={'type': 'date'}),
            'dia_final': TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de grupo de actividades ##

class GrupoForm(ModelForm):

    class Meta:
        model = Grupo
        fields = ['calendario', 'franjas' , 'actividad']

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['calendario'].queryset = Calendario.objects.filter(centro=usuario)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

## Formulario de cambio de contraseña ##

class PasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))