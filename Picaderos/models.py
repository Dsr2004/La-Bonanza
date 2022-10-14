from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from Niveles.models import Nivel
from Estudiantes_Profesores.models import Estudiante, Profesor, Registro

class Picadero(models.Model):
    nombre = models.CharField("Nombre del picadero", max_length=100, unique=True, null=False, blank=False)
    max_estudiantes = models.IntegerField("maximo de estudiantes", null=False, blank=False)
    max_profesores  = models.IntegerField("maximo de profesores", null=False, blank=False)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL,  null=True)
    slug=models.SlugField("Slug", unique=True, null=True, blank=True)

    class Meta:
        db_table = "picaderos"

    def __str__(self):
        return f"{self.nombre}"


class Clase(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, blank=True, null=True)
    estudiante = models.OneToOneField(Registro, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "clases"

    def __str__(self):
        return f"{self.estudiante}"

class InfoPicadero(models.Model):
    picadero = models.ForeignKey(Picadero, on_delete=models.CASCADE)
    hora = models.TimeField()
    clases = models.ManyToManyField(Clase)

    class Meta:
        db_table = "infoPicaderos"

    def __str__(self):
        return f"{self.picadero} a las {self.hora.strftime('%I:%M %p')}"
    
    def get_clases(self):
        print(self)
        # self.clases_set.all()


#SIGNALS
def pre_save_picadero_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.nombre)
        
def pre_save_clase_receiver(sender, instance, *args, **kwargs):
    if  instance.estudiante.profesor:
        instance.profesor = instance.estudiante.profesor
        
def pre_save_infoPicadero_receiver(sender, instance, *args, **kwargs):       
    if instance.hora:
        instance.hora = instance.hora.replace(minute=0, second=0)




pre_save.connect(pre_save_infoPicadero_receiver,sender=InfoPicadero)
pre_save.connect(pre_save_picadero_receiver,sender=Picadero)
pre_save.connect(pre_save_clase_receiver,sender=Clase)

    
    


    