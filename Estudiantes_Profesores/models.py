from django.db import models
from Usuarios.models import Usuario
from multiselectfield import MultiSelectField

DIAS_SEMANA = (
    ("1","Lunes"),("2","Martes"),("3","Miércoles"),("4","Jueves"),("5","Viernes"),("6","Sábado"),("7","Domingo")
)


class Nivel(models.Model):
    nivel = models.CharField(max_length = 150, unique=True, null=False, blank=False)
    color_fondo = models.CharField("color de fondo", null=False, blank=False,max_length = 30)
    color_letra = models.CharField("color de texto", default="rgb(0,0,0)", null=False, blank=False,max_length = 30)

    class Meta:
        db_table = "niveles"
        verbose_name_plural = "niveles"
        

    def __str__(self):
        return self.nivel

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
    nivel = models.ForeignKey(Nivel, db_column="nivel_id", on_delete=models.SET_NULL, verbose_name="nivel del estudiante", null=True)
    #datos para el sistema 
    estado = models.BooleanField(default=True)
    


    class Meta:
        db_table = "estudiantes"

    def __str__(self):
        return self.nombre_completo

    @property
    def get_estudiante(self):
        estudiante = self.nombre_completo.capitalize()
        return estudiante

    
# fecha_inscripcion = models.DateField(auto_now_add=True) to created

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



class Establo(models.Model):
    estudiantes = models.ManyToManyField(Estudiante)
    profesores = models.ManyToManyField(Profesor)
    
    class Meta:
        db_table = "establos"

    def __str__(self):
        return f"{self.pk}"


class Registro(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
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
        return self.estudiante.nivel.nivel

    @property
    def get_dias_clase(self):
        return ["1"]
