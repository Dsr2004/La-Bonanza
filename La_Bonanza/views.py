from django.shortcuts import render
from Usuarios.models import Usuario
from Estudiantes_Profesores.models import Profesor

def index(request):
    Usuarios =  {
        'Usuarios':Usuario.objects.all()
    }
    return render(request, "index.html", Usuarios)
