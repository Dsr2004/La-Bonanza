from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns=[
    path("Calendario/", Calendario.as_view(), name="calendario"),
    path("Estudiantes/", Estudiantes.as_view(), name="estudiantes"),
    path("Profesores/", Profesores.as_view(), name="profesores"),
    path("RegistarEstudiante/", RegistrarEstudiante.as_view(), name="registartEstudiante")
]