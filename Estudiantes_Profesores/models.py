from django.db import models
from Usuarios.models import Usuario
from Niveles.models import Nivel
from multiselectfield import MultiSelectField

DIAS_SEMANA = (
    ("1","Lunes"),("2","Martes"),("3","Miércoles"),("4","Jueves"),("5","Viernes"),("6","Sábado"),("0","Domingo")
)

ESTADOS_ASISTENCIA = (
    ("1","Asistió"),("2","No asistió"),("3","Cancelo con excusa"), ("4", "Cancelo por enfermedad")
)
ESTADOS_CLASES = (
    ("1","Clase puntual"),("2","Mensualidad")
)

def guardar_firma(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/firma-{filename}"
def guardar_documento(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/documento-{filename}"
def guardar_seguro(instance, filename):
    return  f"Archivos_Estudiantes/{instance.nombre_completo}_{instance.documento}/seguro-{filename}"

class Profesor(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=5) 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    horarios = models.CharField("horarios del profesor", max_length=300) # "[{09:00: 18:00},...]"
    niveles = models.ManyToManyField(Nivel)   
    trabaja_sabado = models.BooleanField("el profesor trabaja los sabados", default=False)

    class Meta:
        db_table = "profesores"
        verbose_name_plural = "profesores"

    def __str__(self):
        return self.usuario.nombres



class Estudiante(models.Model):
    nombre_completo = models.CharField("nombre completo", max_length=150, null=False, blank=False)
    fecha_nacimiento = models.DateField("fecha de nacimiento", null=False, blank=False)
    documento = models.CharField("numero de documento", max_length = 18, null=False, blank=False, unique=True)
    celular = models.CharField("numero de celular", max_length = 10, null=False, blank=False)
    telefono = models.CharField("numero de telefono", max_length = 10)
    email = models.EmailField("correo electronico",null=False, blank=False, unique=True)
    direccion = models.CharField("direccion de residencia", max_length = 500,null=False, blank=False,)
    barrio = models.CharField("barrio de resdencia", max_length = 500, null=False, blank=False)
    ciudad = models.CharField("ciudad de residencia",max_length = 150, null=False, blank=False)
    seguro_medico = models.BooleanField("tiene seguro medico", null=False, blank=False)
    documento_identidad =  models.BooleanField("tiene documento de identidad", null=False, blank=False)
    #informacion del acudiente
    nombre_completo_acudiente = models.CharField("nombre completo del acudiente", max_length=150, null=False, blank=False)
    cedula_acudiente = models.CharField("numero de cedula acudiente", max_length = 18, null=False, blank=False, unique=True)
    lugar_expedicion_acudiente = models.CharField("lugar de expedicion de la cedula del acudiente", max_length = 500, null=False, blank=False)
    celular_acudiente = models.CharField("numero de celular acudiente ", max_length = 10)
    email_acudiente = models.EmailField("correo electronico acudiente",null=False, blank=False, unique=True)
    #informacion contacto de emergencia
    nombre_contactoE = models.CharField("nombre del contacto de emergencia", max_length = 10)
    telefono_contactoE = models.CharField("telefono del contacto de emergencia",null=False, blank=False, max_length = 10)
    relacion_contactoE = models.CharField("relacion con el alumno",null=False, blank=False,  max_length = 100)
    #archivos
    firma =models.FileField(upload_to=guardar_firma, null=False, blank=False)
    documento_A =models.FileField(upload_to=guardar_documento, null=False, blank=False)
    seguro_A =models.FileField(upload_to=guardar_seguro, null=False, blank=False) 
    #datos para el sistema
    tipo_clase = models.CharField(max_length=15, choices=ESTADOS_CLASES, null=False, blank=False)
    estado = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        try:
            this = Estudiante.objects.get(id=self.id)
            if this.firma != self.firma:
                this.firma.delete()

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


    def generate_foldername(self, instance, filename):
        return f"{self.nombre_completo}_{self.documento}/"

    @property
    def get_estudiante(self):
        estudiante = self.nombre_completo.capitalize()
        return estudiante

    
# fecha_inscripcion = models.DateField(auto_now_add=True) to created


class Establo(models.Model):
    estudiantes = models.ManyToManyField(Estudiante)
    profesores = models.ManyToManyField(Profesor)
    
    class Meta:
        db_table = "establos"

    def __str__(self):
        return f"{self.pk}"


class Registro(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, db_column="nivel_id", on_delete=models.SET_NULL, verbose_name="nivel del estudiante", null=True)
    profesor = models.ForeignKey(Profesor, db_column="profesor_id", on_delete=models.SET_NULL, verbose_name="profesor del estudiante", null=True)
    pagado = models.BooleanField(default=False)
    inicioClase = models.DateField()
    finClase = models.DateField()
    horaClase = models.TimeField()
    diaClase = MultiSelectField(max_length=10, choices=DIAS_SEMANA)
   

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

    @property
    def get_dias_clase(self):
        dias = []
        for i in self.diaClase:
            dias.append(i)
        return list(dias)


class Asistencia(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, db_column="estudiante_id", verbose_name="estudiante")
    estado = models.CharField(max_length=15,choices=ESTADOS_ASISTENCIA)
    dia = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return self.registro.estudiante.nombre_completo