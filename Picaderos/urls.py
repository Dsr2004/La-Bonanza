from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from Estudiantes_Profesores.views.reportes import ReportePicadero

urlpatterns = [
    path("", login_required(Picaderos.as_view()), name="picaderos"),
    path("InfoPicadero/<slug:slug>", login_required(InfoPicadero.as_view()), name="verPicadero"),
    path("CrearPicadero/", login_required(CrearPicadero.as_view()), name="crearPicadero"),
    path("ModificarPicadero/<int:pk>", login_required(ModificarPicadero.as_view()), name="modificarPicadero"),
    path("BorrarPicadero/", login_required(BorrarPicadero.as_view()), name="borrarPicadero"),
    path("ReportePicadero/<int:pk>", login_required(ReportePicadero.as_view()), name="reportePicadero"),
    
    
]