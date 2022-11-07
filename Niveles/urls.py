from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Niveles, CrearNivel, ModificarNivel, BorrarNivel

urlpatterns = [
    path("Listar/", login_required(Niveles.as_view()), name="listarNivel"),
    path("Crear/", login_required(CrearNivel.as_view()), name="craerNivel"),
    path("Modificar/<int:pk>", login_required(ModificarNivel.as_view()), name="modifcarNivel"),
    path("Borrar/", login_required(BorrarNivel.as_view()), name="borrarNivel"),
] 