from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.es.models import ESIdentityCardNumberField

LISTA_CURSOS = [
        ('3INF', '3 años infantil'),
        ('4INF', '4 años infantil'),
        ('5INF', '5 años infantil'),
        ('1PRI', '1º primaria'),
        ('2PRI', '2º primaria'),
        ('3PRI', '3º primaria'),
        ('4PRI', '4º primaria'),
        ('5PRI', '5º primaria'),
        ('6PRI', '6º primaria'),
    ]

DIAS_SEMANA = (
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miercoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sabado'),
        ('D', 'Domingo'),
)

HORAS_DIA = (
        ('08', '08:00-09:00'),
        ('09', '09:00-10:00'),
        ('10', '10:00-11:00'),
        ('11', '11:00-12:00'),
        ('12', '12:00-13:00'),
        ('13', '13:00-14:00'),
        ('14', '14:00-15:00'),
        ('15', '15:00-16:00'),
        ('16', '16:00-17:00'),
        ('17', '17:00-18:00'),
        ('18', '18:00-19:00'),
        ('19', '19:00-20:00'),
        ('20', '20:00-21:00'),
        ('21', '21:00-22:00'),
)

class Curso(models.Model):    
   
    nombre = models.CharField(max_length=4, choices=LISTA_CURSOS)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):

    es_centro = models.BooleanField(default=False)
    es_tutor = models.BooleanField(default=False)
    es_proveedor = models.BooleanField(default=False)

class Centro(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    provincia = models.CharField(max_length=20)
    localidad = models.CharField(max_length=50)
    codigo = models.CharField(max_length=6, null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    
    def __str__(self):
        return self.usuario.username

class Tutor(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    dni = ESIdentityCardNumberField()
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)

class Proveedor(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nif = ESIdentityCardNumberField()

    def __str__(self):
        return self.usuario.username

class Alumno(models.Model):

    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20)
    edad = models.PositiveSmallIntegerField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Actividad(models.Model):

    nombre = models.CharField(max_length=20)
    min_alumnos = models.PositiveSmallIntegerField()
    max_alumnos = models.PositiveSmallIntegerField()
    precio = models.PositiveSmallIntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cursos = models.ManyToManyField(Curso)
    
    def __str__(self):
        cursos = " ".join(curso.nombre for curso in self.cursos.all())
        return self.nombre + " | " + cursos + " | " + self.proveedor.usuario.username
 
class Franja(models.Model):

    dia = models.CharField(max_length=1, choices=DIAS_SEMANA)
    hora = models.CharField(max_length=2, choices=HORAS_DIA)

    def __str__(self):
        return self.get_dia_display() + " " + self.get_hora_display() # type: ignore

class Calendario(models.Model):

    nombre = models.CharField(max_length=50)
    dia_inicio = models.DateField()
    dia_final = models.DateField()
    plazo_inscripcion = models.BooleanField()
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Grupo(models.Model):

    franjas = models.ManyToManyField(Franja)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(Alumno)
    calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
