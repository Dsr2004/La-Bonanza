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
    ("1","Asistió"),("2","No asistió"),("3","Cancelo con excusa"), ("4", "Cancelo por enfermedad"),("0", "Por validar")
)
ESTADOS_CLASES = (
    ("1","Clase esporádica"),("2","Mensualidad")
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
def guardar_firma(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/firma{extension(filename)}"
def guardar_imagen(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/imagen{extension(filename)}"

def validar_extencion_archivo(value):
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de archivo invalido, solo adjunte archivos .pdf, .jpg, jpeg, .png.')
class Profesor(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=5) 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    horarios = models.CharField("horarios del profesor", max_length=300) 
    niveles = models.ManyToManyField(Nivel)   

    class Meta:
        db_table = "profesores"
        verbose_name_plural = "profesores"

    def __str__(self):
        return self.usuario.get_nombre
    
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
        return f"{self.nombre.capitalize()} {self.get_tipo_clase_display()}"
    


class Estudiante(models.Model):
    primer_nombre = models.CharField("Primer nombre", max_length=50, null=False, blank=False)
    segundo_nombre = models.CharField("Segundo nombre", max_length=50, null=True, blank=True)
    primer_apellido = models.CharField("Primer apellido", max_length=50, null=False, blank=False)
    segundo_apellido = models.CharField("Segundo apellido", max_length=50, null=False, blank=False)
    nombre_completo = models.CharField("nombre completo", max_length=150, null=False, blank=False)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    documento = models.BigIntegerField("número de documento", null=False, blank=False, unique=True)
    celular = models.BigIntegerField("número de celular", null=True, blank=True)
    email = models.EmailField("correo electrónico", unique=True, null=True, blank=True)
    direccion = models.CharField("dirección de residencia", max_length = 500,null=False, blank=False)
    barrio = models.CharField("barrio de resdencia", max_length = 500, null=False, blank=False)
    ciudad = models.CharField("ciudad de residencia",max_length = 150, null=False, blank=False)
    seguro = models.CharField("seguro medico", max_length = 500)
    poliza = models.CharField("poliza",max_length = 150)
    comprobante_seguro_medico = models.BooleanField("tiene comprobante de seguro medico", null=False, blank=False, default=True)
    comprobante_documento_identidad =  models.BooleanField("tiene comprobante de documento de identidad", null=False, blank=False, default=True)
    #informacion de los padres
    # MADRE 
    nombre_completo_madre = models.CharField("nombre completo de la madre", max_length=150, null=True, blank=True)
    cedula_madre = models.IntegerField("número de cédula de la madre", unique=True, null=True, blank=True)
    celular_madre = models.IntegerField("número de celular de la madre", null=True, blank=True)
    email_madre = models.EmailField("correo electrónico de la madre", unique=True, null=True, blank=True)
    # PADRE 
    nombre_completo_padre = models.CharField("nombre completo del padre", max_length=150, null=True, blank=True)
    cedula_padre = models.IntegerField("número de cédula del padre", unique=True, null=True, blank=True)
    celular_padre = models.IntegerField("número de celular del padre ",  null=True, blank=True)
    email_padre = models.EmailField("correo electrónico del padre", unique=True, null=True, blank=True)
    #informacion contacto de emergencia
    nombre_contactoE = models.CharField("nombre del contacto de emergencia", max_length = 100)
    telefono_contactoE = models.IntegerField("telefono del contacto de emergencia",null=False, blank=False)
    relacion_contactoE = models.CharField("relacion con el alumno",null=False, blank=False,  max_length = 100)
    # informacion facturacion
    nombre_facturar = models.CharField("nombre completo a facturar", max_length=150, null=True, blank=True)
    identificacion_facturar = models.IntegerField("número de cédula o nit a facturar", unique=True, null=True, blank=True)
    direccion_facturar = models.CharField("dirección", max_length=500, null=True, blank=True)
    email_facturar = models.EmailField("Correo electrónico a facturar", unique=True, null=True, blank=True)
    telefono_facturar = models.IntegerField('teléfono a facturar', unique=True, null=True, blank=True)
    #archivos
    exoneracion =models.BooleanField(default=False)
    documento_A =models.FileField(upload_to=guardar_documento, validators = [validar_extencion_archivo],null=True, blank=True)
    seguro_A =models.FileField(upload_to=guardar_seguro, validators = [validar_extencion_archivo],null=True, blank=True) 
    # firma poner en NULL FALSE, NO LO PUSE PARA NO TENER QUE BORRAR LOS REGISTROS
    nombrefirma = models.CharField("nombre de la persona que está firmando", max_length=100,null=True, blank=True)
    firma = models.FileField(upload_to=guardar_firma,validators = [validar_extencion_archivo], null=True, blank=True)
    imagen = models.ImageField("Imagen del estudiante", upload_to=guardar_imagen,blank=True, null=True)
    #datos para el sistema
    facturacion_electronica = models.BooleanField("¿Desea facturación electrónica?", default=False)
    tipo_clase = models.CharField(max_length=15, choices=ESTADOS_CLASES, null=False, blank=False)
    tipo_servicio  = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    estado = models.BooleanField(default=True)
    aceptaContrato = models.BooleanField(blank=False, null=False)
    autorizaClub = models.BooleanField(blank=False, null=False)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    nota = models.CharField("Notas", null=True, blank=True, max_length=1000)
    
    def save(self, *args, **kwargs):
        try:
            this = Estudiante.objects.get(id=self.id)
            if this.exoneracion != self.exoneracion:
                this.exoneracion.delete()

            if this.documento_A != self.documento_A:
                this.documento_A.delete()
                
            if this.seguro_A != self.seguro_A:
                this.seguro_A.delete()
                
            if this.imagen != self.imagen:
                this.imagen.delete()
        except: pass
        super(Estudiante, self).save(*args, **kwargs)

    class Meta:
        db_table = "estudiantes"

    def __str__(self):
        return self.get_estudiante

    @property
    def get_estudiante(self):
        if self.segundo_nombre:
            segundo = self.segundo_nombre.lower()
        else:
            segundo = ""
        estudiante = f"{self.primer_nombre.capitalize()} {segundo} {self.primer_apellido.lower()} {self.segundo_apellido.lower()}"
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
    estado = models.CharField(max_length=15,choices=ESTADOS_ASISTENCIA, default=0)
    dia = models.DateField()
    hora = models.TimeField()
    picadero = models.ForeignKey(Picadero, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.registro.estudiante.nombre_completo


 