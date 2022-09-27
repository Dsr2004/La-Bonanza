import calendar
import json
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Estudiante, Registro, Profesor, Asistencia
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
        hora = clases["hora"][0]
        hora = datetime.strptime(hora,"%H:%M").time()
        clases.pop("hora",None)
        clases.pop("csrfmiddlewaretoken",None)
        clasesDia =[]
        for clase in clases:
            clasesDia.append({"estudiante":clases[clase][1],"estado":clases[clase][0]})
        # hasta aqui funciona
        for clase in clasesDia:
            try:
                registro = Registro.objects.get(estudiante=clase["estudiante"])
                asistencia, creado = Asistencia.objects.get_or_create(registro=registro, dia=datetime.now().date(), hora=hora) 
                if creado:
                    asistencia.estado = clase["estado"]
                    asistencia.save()
                    messages.add_message(request, messages.INFO, f"{registro.estudiante.nombre_completo} ha sido registrado correctamente en la asistencia del día")
                else:
                    if asistencia.estado != clase["estado"]:
                        asistencia.estado=clase["estado"]
                        asistencia.save()
                        messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha sido modificado, porque ya estaba en la asistencia del día")
            except:
                 messages.add_message(request, messages.ERROR, f"No se encontro al estudiante en la base de datos")
        return redirect("asistencia")
    
class ControlAsistencia(View):
    model = Asistencia
    template_name = "ctrlAsistencia.html"
    def get(self, request, *args, **kwargs):
        dia = datetime.now().date()
        asistencia = self.model.objects.filter(dia=dia).order_by("hora")
        ctx = {"dia":dia,"asistencia":asistencia}
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        accion = request.POST["accion"]
        dia = request.POST["dia"]
        try:
            dia = datetime.strptime(dia, "%d/%m/%Y")
        except:
            print("error al convertir la fecha")
            return redirect("controlAsistencia")

        if accion == "siguiente":
            dia = dia + timedelta(days=1)
        elif accion == "anterior":
            dia = dia - timedelta(days=1)
        else:
            return redirect("controlAsistencia")
        
        asistencia = self.model.objects.filter(dia=dia).order_by("hora")
        ctx = {"dia":dia,"asistencia":asistencia}
        return render(request, self.template_name, ctx)

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
            contexto={}
            datos=[]
            profe = Profesor.objects.get(pk=request.user.pk)
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
            contexto['Profesor'] = datos[0]
            contexto['Registros'] = Registro.objects.filter(profesor = profe)
            return render(request, self.template_name, contexto)
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

class infoProfesor(ListView):
    template_name = "Profesores/verInfoProfesor.html"
    model = Profesores
    
    def get(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        contexto={}
        datos=[]
        for profe in Profesor.objects.filter(id=kwargs['pk']):
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
            datos.append({'profesor':profe, 'horarios':horario.split(', ')})
        contexto['Profesor'] = datos
        return render(request, self.template_name, contexto)

class editProfesor(TemplateView):
    template_name = "Profesores/editProfesor.html"
    model = Profesor
    form_class=ProfesorForm
    
    def get(self, request, *args, **kwargs):
        contexto = {}
        try:
            get_object = Usuario.objects.get(pk=kwargs['pk'])
            if kwargs['pk']==request.user.pk:  
                return redirect('index')
        except:
            return redirect('index')
        form = self.form_class(request.POST or None, instance=get_object)
        datos=[]
        for profe in Profesor.objects.filter(id=kwargs['pk']):
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
            datos.append({'profesor':profe, 'horarios':horario.split(', ')})
        contexto['Profesor'] = datos[0]
        contexto['horarios'] = json.loads(datos[0]['profesor'].horarios)
        contexto['horarios'] = json.dumps(contexto['horarios'])
        contexto['form'] = form
        
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        try:
            datos = json.loads(request.POST.get('datos'))
            profesor = self.model.objects.get(pk = kwargs['pk'])
            profesor.horarios = json.dumps(json.loads(datos['horarios']))
            niveles = datos['niveles']
            profesor.niveles.clear()
            for nivel in niveles:
                profesor.niveles.add(nivel)
            profesor.trabaja_sabado = datos['trabaja_sabado']
            profesor.save()
            return JsonResponse({"datos":'Se modifico correctamente'})
        except Exception as e:
            data = json.dumps({'error': 'No se pudo modificar la información del usuario por {error}'.format(error=e)})
            return HttpResponse(data, content_type="application/json", status=400)

class estudiantesProfesor(TemplateView):
    template_name = "Profesores/estudiantesProfesor.html"
    
    def get(self, request, *args, **kwargs):
        profesor = Profesor.objects.get(id=kwargs['pk'])
        response = {'Registros': Registro.objects.filter(profesor = profesor), 'Profesor':profesor}
        return render(request, self.template_name, response)
    def post(self, request, *args, **kwargs):
        if request.POST.get('tipo')=="delete":
            registro = Registro.objects.get(pk = request.POST.get('estudiante'))
            try:
                registro.profesor = None
                registro.save()
                return JsonResponse({"profesor":'hola'})
            except:
                data = json.dumps({'error': 'No se pudo remover el estudiante '+registro.estudiante})
                return HttpResponse(data, content_type="application/json", status=400)
        if request.POST.get('tipo') == 'add':
            estudiantes = json.loads(request.POST.get('estudiantes'))
            profesor=Profesor.objects.get(pk = kwargs['pk'])
            for estudiante in estudiantes:
                registro = Registro.objects.get(pk = int(estudiante))
                registro.profesor = profesor
                registro.save()
            return JsonResponse({"profesor":'hola'})
        else:
            data = json.dumps({'error': 'No se ha enviado un tipo valido para esta solicitud'})
            return HttpResponse(data, content_type="application/json", status=400)
class agregarEstudiantesProfesor(ListView):
    template_name = "Profesores/agregarEstudiantes.html"
    
    def get(self,request, *args, **kwargs):
        profesor = Profesor.objects.get(pk = kwargs['pk'])
        registros = Registro.objects.exclude(profesor=profesor)
        context = {}
        context["profesor"] = profesor
        context["registros"] = registros
        return render(request, self.template_name, context)
    
class estudianteProfesor(ListView):
    template_name = "Profesores/estudianteProfesor.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['registro'] = Registro.objects.get(pk=request.GET.get('id_registro'))
        context['profesor'] = Profesor.objects.get(id=kwargs['pk'])
        context['horaClase'] = datetime.strptime(str(context['registro'].horaClase), '%H:%M:%S').strftime('%I:%M %p')
        return render(request, self.template_name, context)

def datosProfesores(request):
    if request.user.administrador!=1:
        return redirect("calendario")
    if request.method == 'POST':
        profesor = json.loads(request.POST.get('datos'))
        user = request.POST.get('usuario')
        user=Usuario.objects.get(id = user)
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
                user.delete()
                data = json.dumps({'error': 'Datos del profesor ingresados incorrectos', 'forms':form.errors})
                return HttpResponse(data, content_type="application/json", status=400)
        else:
            user.delete()
            data = json.dumps({'error': 'Datos del profesor ingresados incorrectos', 'forms':form.errors})
            return HttpResponse(data, content_type="application/json", status=400)
    return HttpResponse('Solo se admiten post', content_type="application/json", status=400)