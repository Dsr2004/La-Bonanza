from django.contrib import admin
from .models import Estudiante, Registro, Profesor, Asistencia, Calendario, Servicio

admin.site.register(Estudiante)
admin.site.register(Registro)
admin.site.register(Profesor)
admin.site.register(Asistencia)
admin.site.register(Calendario)
admin.site.register(Servicio)
