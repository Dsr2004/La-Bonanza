from django.urls import path
# from django.contrib.auth.decorators import login_required
from .views import *
from django.contrib.auth.decorators import login_required



urlpatterns=[
    path("Calendario/", Calendario.as_view(), name="calendario"),
    path("Estudiantes/", Estudiantes.as_view(), name="estudiantes"),
    path("Profesores/", Profesores.as_view(), name="profesores"),
    path("RegistarEstudiante/", RegistrarEstudiante.as_view(), name="registrarEstudiante"),
    path("BuscarNuevosEstudiantes/", BuscarNuevosEstudiantes.as_view(), name="buscarNuevosEstudiantes"),
    path("CrearNuevosEstudiantes/<int:pk>", CrearNuevosEstudiantes.as_view(), name="crearNuevosEstudiantes"),
    path("ValidarRegistroEstudiante/", ValidarRegistroEstudiante.as_view(), name="validarRegistroEstudiante"),
    path("VerInfoEstudiante/<int:pk>", login_required(VerInfoEstudiante.as_view()), name="verInfoEstudiante"),
    path("ModificarEstudiante/<int:pk>", login_required(ModificarEstudiante.as_view()), name="modificarEstudiante"),
    path("ModificarRegistroEstudiante/<int:pk>", login_required(ModificarRegistroEstudiante.as_view()), name="modificarRegistroEstudiante"),
    path("CambiarEstadoEstudiante/", login_required(CambiarEstadoEstudiante.as_view()), name="cambiarEstadoEstudiante"),
    path('registrarProfesor/', login_required(datosProfesores), name="registrarProfesor"),
    path('VerInfoProfesor/<str:pk>', login_required(infoProfesor.as_view()), name="verInfoProfesor"),
    path('editarProfesor/<str:pk>', login_required(editProfesor.as_view()), name="editarProfesor"),
    path('VerEstudiantes/<str:pk>', login_required(estudiantesProfesor.as_view()), name="verEstudiantes"),
    path('VerEstudiante/<str:pk>', login_required(estudianteProfesor.as_view()), name="verEstudiante"),
    path('agregarEstudiante/<str:pk>', login_required(agregarEstudiantesProfesor.as_view()), name="agregarEstudiante"),
    path("VerInfoEstudianteCalendario/<int:pk>", login_required(VerInfoEstudianteCalendario.as_view()), name="verInfoEstudianteCalendario"),
    path("Asistencia/", login_required(GestionDeAsistencia.as_view()), name="asistencia"),
    path("ControlAsistencia/", login_required(ControlAsistencia.as_view()), name="controlAsistencia"),
]