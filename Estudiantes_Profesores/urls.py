from django.urls import path
from django.contrib.auth.decorators import login_required
from .views.views import *
from .views.estudiantes import *
from .views.profesores import *
from .views.reportes import reporteEstudiantes, reporteAsistencia



urlpatterns=[
    path("Calendario/", login_required(Calendario.as_view()), name="calendario"),
    path("Estudiantes/", login_required(Estudiantes.as_view()), name="estudiantes"),
    path("Profesores/", login_required(Profesores.as_view()), name="profesores"),
    path("RegistarEstudiante/", RegistrarEstudiante.as_view(), name="registrarEstudiante"),
    path("BuscarNuevosEstudiantes/", login_required(BuscarNuevosEstudiantes.as_view()), name="buscarNuevosEstudiantes"),
    path("CrearNuevosEstudiantes/<int:pk>", login_required(CrearNuevosEstudiantes.as_view()), name="crearNuevosEstudiantes"),
    path("ValidarRegistroEstudiante/", login_required(ValidarRegistroEstudiante.as_view()), name="validarRegistroEstudiante"),
    path("VerInfoEstudiante/<int:pk>", login_required(VerInfoEstudiante.as_view()), name="verInfoEstudiante"),
    path("VerInfoEstudianteSinRegistro/<int:pk>", login_required(VerInfoEstudianteSinRegistro.as_view()), name="verInfoEstudianteSinRegistro"),
    path("ModificarEstudiante/<int:pk>", login_required(ModificarEstudiante.as_view()), name="modificarEstudiante"),
    path("ModificarDocsEstudiante/<int:pk>", login_required(ModificarDocsEstudiante.as_view()), name="modificarDocsEstudiante"),
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
    path("ReporteEstudiantes/", login_required(reporteEstudiantes.as_view()), name="reporteEstudiantes"),
    path("ReporteAsistencias/", login_required(reporteAsistencia.as_view()), name="reporteAsistencia"),
    path("ConteoClasesFecha/<int:pk>", login_required(ConteoClasesFecha.as_view()), name="conteoClasesFecha"),
    path("ClasesCanceladas/", login_required(ClasesCanceladas.as_view()), name="clasesCanceladas"),
    path("ReponerClase/<int:pk>", login_required(ReponerClase.as_view()), name="reponerClase"),
]