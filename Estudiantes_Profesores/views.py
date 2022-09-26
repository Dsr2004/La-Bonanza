import calendar
import json
from pprint import pprint
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from .models import Estudiante, Registro, Profesor
from .forms import EstudianteForm, RegistroForm,ProfesorForm
from Usuarios.models import Usuario
from datetime import datetime, timedelta
from itertools import groupby



def arreglarFormatoDia(dia):
    if str(dia) == "6":
        dia = 0 #en las variables del modelo el domingo es 0 porque asi lo recibe fullcalendar pero python retorna el domingo como 6
    else:
        dia = dia+1
    return dia

class Calendario(View):
    template_name = "calendario.html"
    model = Registro
    def get(self, request, *args, **kwargs):
        registros = Registro.objects.all()
        ctx = {"clases":registros}
        return render(request, self.template_name ,ctx)

class VerInfoEstudianteCalendario(DetailView):
    model=Registro
    template_name = "Calendario/verInfoEstudianteCalendario.html"


class GestionDeAsistencia(View):
    template_name = "asistencia.html"
    model = Registro
    def get(self, request, *args, **kwargs):
        ctx = {}
        hoy = datetime.now()
        diaSemana = arreglarFormatoDia(hoy.weekday())
        clasesHoy = Registro.objects.filter(diaClase__icontains=diaSemana).order_by("horaClase")
        
        ctx["dia"]=hoy.date()
        ctx["hora"]=hoy.time()
        ctx["clases"]=clasesHoy
        # mañana = hoy + timedelta(days=6)
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        clases = dict(request.POST.copy())
        hora = clases["hora"]
        print(hora)
        clases.pop("hora",None)
        clases.pop("csrfmiddlewaretoken",None)
        kiwi =[]
        for clase in clases:
            kiwi.append({"estudiante":clases[clase][1],"estado":clases[clase][0]})
        print(kiwi)
        return HttpResponse(request.POST)
    

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

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
        

    
class BuscarNuevosEstudiantes(View):
     def get(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
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

class VerInfoEstudiante(DetailView):
    model=Estudiante
    template_name = "Estudiantes/verInfoEstudiante.html"
    
    def get_context_data(self, **kwargs):
        contexto =  super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        registro = Registro.objects.get(estudiante=estudiante)
        contexto["registro"] = registro
        return contexto

class ModificarEstudiante(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "Estudiantes/editarInfoEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        registro = Registro.objects.get(estudiante=estudiante)
        contexto["registro"] = registro
        contexto["formRegistro"] = RegistroForm(instance=registro)
        return contexto


    def form_invalid(self, form):
       return JsonResponse({"errores": form.errors}, status=404)

class CambiarEstadoEstudiante(View):
    def post(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        estudiante = Estudiante.objects.get(pk=request.POST["id"])
        if estudiante.estado == True:
            estudiante.estado = False
        else:
            estudiante.estado = True
        estudiante.save()

        return JsonResponse({"mensaje":"estudiante modificado con exito"}, status=200)

class ValidarRegistroEstudiante(View):
    def post(self, request, *args, **kwargs):
        dia = request.POST.get("dia")[2]
        print(dia)
        estudiante = request.POST.get("estudiante")
        estudiante = Estudiante.objects.get(pk=estudiante)
        estudiantesDia = Registro.objects.filter(diaClase__icontains=dia)
        estudiantesDia = Estudiante.objects.filter(pk__in = [x.id for x in estudiantesDia])
        estudiantesDia = int(estudiantesDia.filter(nivel=estudiante.nivel.id).count())
        return JsonResponse({"cant":estudiantesDia, "nivel":estudiante.nivel.nivel})

class ModificarRegistroEstudiante(UpdateView):
    model = Registro
    form_class = RegistroForm
    template_name = "Estudiantes/editarInfoEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def form_invalid(self, form):
        print(form.errors)
        return JsonResponse({"errores": form.errors}, status=404)


class Profesores(ListView):
    template_name = "profesores.html"
    model = Profesor
    
    def get(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        contexto={}
        datos=[]
        for profe in Profesor.objects.all():
            horario = []
            try:
                horarios = json.loads(profe.horarios)
                for horas in horarios:
                    desde = datetime.strptime(horas['from'], '%H:%M').strftime('%I:%M %p')
                    hasta=datetime.strptime(horas['through'], '%H:%M').strftime('%I:%M %p')
                    horario.append('Desde '+str(desde)+' Hasta '+str(hasta))
            except:
                horario.append('Este profesor no tiene horario')
            horario = str(horario).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            datos.append({'profesor':profe, 'horario':horario})
        contexto['Profesores'] = datos
        return render(request, self.template_name, contexto)

def datosProfesores(request):
    if request.user.administrador!=1:
        return redirect("calendario")
    if request.method == 'POST':
        profesor = json.loads(request.POST.get('datos'))
        user = json.loads(request.POST.get('usuario'))
        user=Usuario.objects.get(pk = user)
        formObject = {'niveles':profesor['niveles'],'trabaja_sabado':profesor['trabaja_sabado']}
        form = ProfesorForm(formObject or None)
        if form.is_valid():
            try:
                horarios = profesor.get('horarios')
                horarios = json.dumps(json.loads(horarios))
                saba = form.cleaned_data['trabaja_sabado']
                profesorModel = Profesor.objects.create(pk=user.pk,usuario = user,horarios=horarios, trabaja_sabado=saba)
                niveles = form.cleaned_data['niveles']
                for nivel in niveles:
                    profesorModel.niveles.add(nivel)
                return JsonResponse({"profesor":profesor,'usuario':user.usuario})
            except Exception as e:
                print(e)
                user.delete()
                data = json.dumps({'error': 'Datos del profesor ingresados incorrectos', 'forms':form.errors})
                return HttpResponse(data, content_type="application/json", status=400)
        else:
            user.delete()
            data = json.dumps({'error': 'Datos del profesor ingresados incorrectos', 'forms':form.errors})
            return HttpResponse(data, content_type="application/json", status=400)
    return HttpResponse('Solo se admiten post', content_type="application/json", status=400)