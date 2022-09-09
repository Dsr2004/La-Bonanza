from django.urls import path
# from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns=[
    path("Calendario/", Calendario.as_view(), name="calendario"),
    path("Estudiantes/", Estudiantes.as_view(), name="estudiantes"),
    path("Profesores/", Profesores.as_view(), name="profesores"),
    path("RegistarEstudiante/", RegistrarEstudiante.as_view(), name="registrarEstudiante"),
    path("BuscarNuevosEstudiantes/", BuscarNuevosEstudiantes.as_view(), name="buscarNuevosEstudiantes"),
    path("CrearNuevosEstudiantes/<int:pk>", CrearNuevosEstudiantes.as_view(), name="crearNuevosEstudiantes"),
    path("ValidarRegistroEstudiante/", ValidarRegistroEstudiante.as_view(), name="validarRegistroEstudiante"),
    path("VerInfoEstudiante/<int:pk>", VerInfoEstudiante.as_view(), name="verInfoEstudiante"),
]