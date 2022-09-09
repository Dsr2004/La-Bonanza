from calendar import c
from django.shortcuts import render
from django.views.generic import View, CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
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

class ValidarRegistroEstudiante(View):
    def post(self, request, *args, **kwargs):
        dia = request.POST.get("dia")
        estudiante = request.POST.get("estudiante")
        estudiante = Estudiante.objects.get(pk=estudiante)
        estudiantesDia = Registro.objects.filter(diaClase=dia)
        estudiantesDia = Estudiante.objects.filter(pk__in = [x.id for x in estudiantesDia])
        estudiantesDia = int(estudiantesDia.filter(nivel=estudiante.nivel.id).count())
        return JsonResponse({"cant":estudiantesDia, "nivel":estudiante.nivel.nivel})

class VerInfoEstudiante(DetailView):
    model=Estudiante
    template_name = "Estudiantes/verInfoEstudiante.html"
    
    def get_context_data(self, **kwargs):
        contexto =  super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        registro = Registro.objects.get(estudiante=estudiante)
        contexto["registro"] = registro
        return contexto


class Profesores(ListView):
    template_name = "profesores.html"
    model = Profesor