from django.shortcuts import render
from django.views.generic import View, CreateView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Exists
from .models import Estudiante, Registro, Profesor
from .forms import EstudianteForm, RegistroForm

class Calendario(View):
    template_name = "calendario.html"
    model = Registro
    def get(self, request, *args, **kwargs):
        registros = Registro.objects.all()
        ctx = {"clases":registros}
        return render(request, self.template_name ,ctx)

class Estudiantes(ListView):
    template_name = "estudiantes.html"
    context_object_name= "estudiantes"
    model = Registro

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        estudiantes = Estudiante.objects.all().count()
        registrosEstudiantes = self.model.objects.all().count()
        if estudiantes != registrosEstudiantes:
            ctx["nuevosEstudiantes"]=True
        else:
             ctx["nuevosEstudiantes"]=False
        return ctx

class RegistrarEstudiante(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "crearEstudiante.html"
    success_url = reverse_lazy("estudiantes")
    
class BuscarNuevosEstudiantes(View):
     def get(self, request, *args, **kwargs):
        EstudiantesConRegisto = Estudiante.objects.all()
        EstudiantesSinRegisto = []
        for registro in EstudiantesConRegisto:
            if not hasattr(registro, "registro"):
               EstudiantesSinRegisto.append(registro)
        ctx={"estudiantes":EstudiantesSinRegisto}
        return render(request, "Estudiantes/estudiantesSinRegistro.html", ctx)

class CrearNuevosEstudiantes(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = "Estudiantes/RegistroEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        ctx["estudiante"] = estudiante
        return ctx

    
class Profesores(ListView):
    template_name = "profesores.html"
    model = Profesor