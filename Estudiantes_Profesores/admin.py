from django.contrib import admin
from .models import Estudiante, Registro, Profesor, Asistencia, Calendario

admin.site.register(Estudiante)
admin.site.register(Registro)
admin.site.register(Profesor)
admin.site.register(Asistencia)
admin.site.register(Calendario)
