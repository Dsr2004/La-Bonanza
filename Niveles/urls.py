from django.urls import path
from .views import Niveles, CrearNivel, ModificarNivel, BorrarNivel

urlpatterns = [
    path("Listar/", Niveles.as_view(), name="listarNivel"),
    path("Crear/", CrearNivel.as_view(), name="craerNivel"),
    path("Modificar/<int:pk>", ModificarNivel.as_view(), name="modifcarNivel"),
    path("Borrar/", BorrarNivel.as_view(), name="borrarNivel"),
] 