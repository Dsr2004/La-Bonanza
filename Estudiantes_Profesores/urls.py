from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns=[
    path("Calendario/", Calendario.as_view(), name="calendario"),
    path("RegistarEstudiante/", RegistrarEstudiante.as_view(), name="registartEstudiante")
]