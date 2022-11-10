import os
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.core.validators import MaxValueValidator
from Picaderos.models import Clase, InfoPicadero, Picadero
from Usuarios.models import Usuario
from Niveles.models import Nivel
import json
from datetime import datetime, date, timedelta
def DIA_INGLES(dia):
    dias = {"Monday":"Lunes","Tuesday":"Martes","Wednesday":"Miércoles","Thursday":"Jueves","Friday":"Viernes","Saturday":"Sábado","Sunday":"Domingo"}
    dia = dias.get(str(dia))
    return dia

DIAS_SEMANA = (
    ("1","Lunes"),("2","Martes"),("3","Miércoles"),("4","Jueves"),("5","Viernes"),("6","Sábado"),("0","Domingo")
)

ESTADOS_ASISTENCIA = (
    ("1","Asistió"),("2","No asistió"),("3","Cancelo con excusa"), ("4", "Cancelo por enfermedad")
)
ESTADOS_CLASES = (
    ("1","Clase puntual"),("2","Mensualidad")
)
def extension(file):
        name, extension = os.path.splitext(file)
        return extension


def guardar_exoneracion(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/exoneracion{extension(filename)}"
def guardar_documento(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/documento{extension(filename)}"
def guardar_seguro(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/seguro{extension(filename)}"

def validar_extencion_archivo(value):
    
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de archivo invalido, solo adjunte archivos .pdf, .jpg, jpeg, .png.')
class Profesor(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=5) 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    horarios = models.CharField("horarios del profesor", max_length=300) # "[{"day": "Lunes","from": "11:42", "through": "23:42"},...]"
    niveles = models.ManyToManyField(Nivel)   
    trabaja_sabado = models.BooleanField("el profesor trabaja los sabados", default=False)

    class Meta:
        db_table = "profesores"
        verbose_name_plural = "profesores"

    def __str__(self):
        return self.usuario.nombres
    @property
    def get_days(self):
        days = []
        horarios = json.loads(self.horarios)
        for horario in horarios:
            days.append(horario.get('day'))
        return days
    @property
    def get_hora_inicial(self):
        horas = []
        horarios = json.loads(self.horarios)
        for horario in horarios:
            day = datetime.strptime(horario.get('from'), '%H:%M')
            horas.append(day.strftime('%H:%M %p'))
        return horas
    @property
    def get_hora_final(self):
        horas = []
        horarios = json.loads(self.horarios)
        for horario in horarios:
            day = datetime.strptime(horario.get('through'), '%H:%M')
            horas.append(day.strftime('%H:%M %p'))
        return horas
    @property
    def get_profesor(self):
        return f"{self.usuario.nombres.capitalize()} {self.usuario.apellidos.capitalize()}"
    
class Servicio(models.Model):
    nombre = models.CharField("Nombre del servicio", max_length=55, null=False, blank=False)
    descripcion = models.CharField("Descripción del servicio", max_length=50, null=True, blank=True)
    tipo_clase = models.CharField(max_length=15, choices=ESTADOS_CLASES, null=False, blank=False)

    def __str__(self):
        return self.descripcion
    


class Estudiante(models.Model):
    nombre_completo = models.CharField("nombre completo", max_length=150, null=False, blank=False)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    documento = models.IntegerField("numero de documento", null=False, blank=False, unique=True)
    celular = models.IntegerField("numero de celular", null=True, blank=True)
    email = models.EmailField("correo electronico", unique=True, null=True, blank=True)
    direccion = models.CharField("direccion de residencia", max_length = 500,null=False, blank=False,)
    barrio = models.CharField("barrio de resdencia", max_length = 500, null=False, blank=False)
    ciudad = models.CharField("ciudad de residencia",max_length = 150, null=False, blank=False)
    seguro = models.CharField("seguro medico", max_length = 500)
    poliza = models.CharField("poliza",max_length = 150)
    comprobante_seguro_medico = models.BooleanField("tiene comprobante de seguro medico", null=False, blank=False)
    comprobante_documento_identidad =  models.BooleanField("tiene comprobante de documento de identidad", null=False, blank=False)
    #informacion de los padres
    # MADRE 
    nombre_completo_madre = models.CharField("nombre completo de la madre", max_length=150, null=True, blank=True)
    cedula_madre = models.IntegerField("numero de cedula de la madre", unique=True, null=True, blank=True)
    lugar_expedicion_madre = models.CharField("lugar de expedicion de la cedula de la madre", max_length = 500, null=True, blank=True)
    celular_madre = models.IntegerField("numero de celular de la madre", null=True, blank=True)
    email_madre = models.EmailField("correo electronico de la madre", unique=True, null=True, blank=True)
    # PADRE 
    nombre_completo_padre = models.CharField("nombre completo del padre", max_length=150, null=True, blank=True)
    cedula_padre = models.IntegerField("numero de cedula del padre", unique=True, null=True, blank=True)
    lugar_expedicion_padre = models.CharField("lugar de expedicion de la cedula del padre", max_length = 500, null=True, blank=True)
    celular_padre = models.IntegerField("numero de celular del padre ",  null=True, blank=True)
    email_padre = models.EmailField("correo electronico del padre", unique=True, null=True, blank=True)
    direccion_A = models.CharField("direccion de residencia", max_length = 500,null=True, blank=True)
    barrio_A = models.CharField("barrio de resdencia", max_length = 500, null=True, blank=True)
    ciudad_A = models.CharField("ciudad de residencia",max_length = 150, null=True, blank=True)
    #informacion contacto de emergencia
    nombre_contactoE = models.CharField("nombre del contacto de emergencia", max_length = 10)
    telefono_contactoE = models.IntegerField("telefono del contacto de emergencia",null=False, blank=False)
    relacion_contactoE = models.CharField("relacion con el alumno",null=False, blank=False,  max_length = 100)
    #archivos
    exoneracion =models.FileField(upload_to=guardar_exoneracion, validators = [validar_extencion_archivo],null=False, blank=False)
    documento_A =models.FileField(upload_to=guardar_documento, validators = [validar_extencion_archivo],null=False, blank=False)
    seguro_A =models.FileField(upload_to=guardar_seguro, validators = [validar_extencion_archivo],null=False, blank=False) 
    #datos para el sistema
    facturacion_electronica = models.BooleanField("¿Desea facturación electrónica?", default=False)
    tipo_clase = models.CharField(max_length=15, choices=ESTADOS_CLASES, null=False, blank=False)
    tipo_servicio  = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    estado = models.BooleanField(default=True)
    aceptaContrato = models.BooleanField(blank=False, null=False)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        try:
            this = Estudiante.objects.get(id=self.id)
            if this.exoneracion != self.exoneracion:
                this.exoneracion.delete()

            if this.documento_A != self.documento_A:
                this.documento_A.delete()
                
            if this.seguro_A != self.seguro_A:
                this.seguro_A.delete()
        except: pass
        super(Estudiante, self).save(*args, **kwargs)

    class Meta:
        db_table = "estudiantes"

    def __str__(self):
        return self.nombre_completo

    @property
    def get_estudiante(self):
        estudiante = self.nombre_completo.capitalize()
        return estudiante
    @property
    def get_edad(self):
        hoy = date.today()
        nacimiento = self.fecha_nacimiento
        if hoy.year == nacimiento.year:
            edad = hoy.month - nacimiento.month -  ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
            if edad == 1:
                edad = f"{edad} Mes"
            else:
                edad = f"{edad} Meses"
        else:
            edad = hoy.year - nacimiento.year -  ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)) 
            if edad == 1:
                edad = f"{edad} Año"
            else:
                edad = f"{edad} Años"
        return edad 



class Registro(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, db_column="nivel_id", on_delete=models.SET_NULL, verbose_name="nivel del estudiante", null=True)
    profesor = models.ForeignKey(Profesor, db_column="profesor_id", on_delete=models.SET_NULL, verbose_name="profesor del estudiante",null=True)
    pagado = models.BooleanField(default=False)
   

    class Meta:
        db_table = "registros"

    def __str__(self):
        return self.estudiante.nombre_completo

    @property
    def get_estado_matricula(self):
        if self.pagado:
            return "Pagada"
        else:
            return "Pendiente"

    @property
    def get_estudiante(self):
        estudiante = self.estudiante.nombre_completo.capitalize()
        return estudiante

    @property
    def get_estudiante_documento(self):
        return self.estudiante.documento

    @property
    def get_estudiante_celular(self):
        return self.estudiante.celular


    @property
    def get_estudiante_nivel(self):
        return self.nivel.nivel

    # @property
    # def get_dias_clase(self):
    #     dias = []
    #     for i in self.diaClase:
    #         dias.append(i)
    #     return list(dias)


class Calendario(models.Model):
    diaClase = models.CharField(max_length=10, choices=DIAS_SEMANA)
    inicioClase = models.DateField()
    finClase = models.DateField()
    horaClase = models.TimeField()
    estado = models.BooleanField(default=True)
    registro = models.ForeignKey(Registro, db_column="registro_id", on_delete=models.CASCADE, verbose_name="registro", null=True, blank=True)
    
    
    def __str__(self):
        return f"C-{self.registro.estudiante.get_estudiante} el dia {self.get_diaClase_display()} a las {self.horaClase.strftime('%I:%M %p')}"
class Asistencia(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, db_column="estudiante_id", verbose_name="estudiante")
    estado = models.CharField(max_length=15,choices=ESTADOS_ASISTENCIA)
    dia = models.DateField()
    hora = models.TimeField()
    picadero = models.ForeignKey(Picadero, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.registro.estudiante.nombre_completo

# SIGNALS 
    
            
# def post_save_registro_receiver(sender, instance, created, **kwargs):
#     if created:
#         picadero =  Picadero.objects.get(nivel=instance.nivel)
#         clase =  Clase.objects.create(estudiante=instance, profesor=instance.profesor)
#         clase.save()
#         for dia in instance.diaClase:
#             iPicadero, creado = InfoPicadero.objects.get_or_create(picadero=picadero,hora=instance.horaClase, dia=dia) 
#             iPicadero.save()
#             iPicadero.clases.add(clase)
        

# pre_save.connect(pre_save_registro_receiver,sender=Registro)
# post_save.connect(post_save_registro_receiver,sender=Registro)
