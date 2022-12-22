from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from Niveles.models import Nivel
from datetime import date, datetime, timedelta
from django.utils import timezone


DIAS_SEMANA = (
    ("1","Lunes"),("2","Martes"),("3","Miércoles"),("4","Jueves"),("5","Viernes"),("6","Sábado"),("0","Domingo")
)

class Picadero(models.Model):
    nombre = models.CharField("Nombre del picadero", max_length=100, unique=True, null=False, blank=False)
    max_estudiantes = models.IntegerField("maximo de estudiantes", null=False, blank=False)
    max_profesores  = models.IntegerField("maximo de profesores", null=False, blank=False)
    nivel = models.OneToOneField(Nivel, on_delete=models.SET_NULL,  null=True)
    slug = models.SlugField("Slug", unique=True, null=True, blank=True)
    # creado = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "picaderos"

    def __str__(self):
        return f"{self.nombre}"


class Clase(models.Model):
    profesor = models.ForeignKey(to="Estudiantes_Profesores.Profesor", on_delete=models.SET_NULL, blank=True, null=True)
    calendario = models.ForeignKey(to="Estudiantes_Profesores.Calendario", on_delete=models.CASCADE)
    class Meta:
        db_table = "clasesOlvidadas"

    def __str__(self):
        return f"{self.calendario.registro.get_estudiante}"
    
class InfoPicadero(models.Model):
    picadero = models.ForeignKey(Picadero, on_delete=models.CASCADE)
    dia = models.CharField(max_length=15, choices=DIAS_SEMANA)
    hora = models.TimeField()
    clases = models.ManyToManyField(Clase, through='EstadoClase')

    class Meta:
        db_table = "infoPicaderos"

    def __str__(self):
        return f"{self.picadero} el dia {self.get_dia_display()} a las {self.hora.strftime('%I:%M %p')}"
    
    def get_clases(self):
        print(self)
        # self.clases_set.all()



class EstadoClase(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    InfoPicadero = models.ForeignKey(InfoPicadero, on_delete=models.CASCADE)
    dia = models.DateField(default=timezone.now)
    estado = models.BooleanField(default=True)
    fecha_cancelacion = models.DateField(null=True, blank=True)
    
    class Meta():
        db_table="HistorialClases"
    
    def __str__(self):
        return f'clase {self.clase} relacionada {self.InfoPicadero} dia {self.dia}'
    
    @property
    def get_date_time(self):
        return f"{self.dia.strftime('%Y-%m-%d')}T{self.InfoPicadero.hora}"
    

#SIGNALS
def pre_save_picadero_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.nombre)
        
def pre_save_clase_receiver(sender, instance, *args, **kwargs):
    print(instance.calendario.registro.profesor)
    if  not instance.calendario.registro.profesor:
        instance.profesor = instance.calendario.registro.profesor
        
def pre_save_infoPicadero_receiver(sender, instance, *args, **kwargs):       
    if instance.hora:
        instance.hora = instance.hora.replace(minute=0, second=0)




pre_save.connect(pre_save_infoPicadero_receiver,sender=InfoPicadero)
pre_save.connect(pre_save_picadero_receiver,sender=Picadero)
pre_save.connect(pre_save_clase_receiver,sender=Clase)

    
    


    