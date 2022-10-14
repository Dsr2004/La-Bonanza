from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path("", login_required(Picaderos.as_view()), name="picaderos"),
    path("InfoPicadero/<slug:slug>", login_required(InfoPicadero.as_view()), name="verPicadero"),
    path("CrearPicadero/", login_required(CrearPicadero.as_view()), name="crearPicadero"),
]