from django.shortcuts import render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from .models import Estudiante, Registro
from .forms import EstudianteForm, RegistroForm

class Calendario(View):
    template_name = "calendario.html"
    model = Registro
    def get(self, request, *args, **kwargs):
        registros = Registro.objects.all()
        ctx = {"clases":registros}
        return render(request, self.template_name ,ctx)

class RegistrarEstudiante(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "crearEstudiante.html"
    success_url = reverse_lazy("calendario")