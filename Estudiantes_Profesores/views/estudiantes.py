import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from La_Bonanza. mixins import IsAdminMixin
from Niveles.models import Nivel
from Picaderos.models import EstadoClase, Picadero, InfoPicadero, Clase
from ..models import Estudiante, Registro, Profesor, Calendario as CalendarioModel
from ..forms import EstudianteForm,CrearEstudianteForm, RegistroForm,ProfesorForm
from ..models import DIAS_SEMANA
from .views import arreglarFormatoDia, serialiserValidation

class Estudiantes(IsAdminMixin, ListView):
    template_name = "estudiantes.html"
    context_object_name= "estudiantes"
    model = Registro
    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        estudiantes = Estudiante.objects.all().count()
        registrosEstudiantes = self.model.objects.all().count()
        ctx['niveles'] = Nivel.objects.all()
        if estudiantes != registrosEstudiantes:
            ctx["nuevosEstudiantes"]=True
        else:
            ctx["nuevosEstudiantes"]=False
        return ctx
    

class RegistrarEstudiante(CreateView):
    model = Estudiante
    form_class = CrearEstudianteForm
    template_name = "crearEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if self.request.user.administrador:
                form.save()
                return redirect("estudiantes")
        else:
            nombre = str(form.cleaned_data['nombre_completo']).capitalize()
            form.save()
            return render(self.request, "gracias.html",{"nombre":nombre})

        return super().form_valid(form)
    

class BuscarNuevosEstudiantes(IsAdminMixin, View):
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

class CrearNuevosEstudiantes(IsAdminMixin, CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = "Estudiantes/RegistroEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        ctx["estudiante"] = estudiante
        return ctx
    
    def post(self, request, *args, **kwargs):
        copia = request.POST.copy()
        dia = request.POST.get('inicioClase')
        diaOriginal = dia
        if not dia:
            return JsonResponse({"errores":{"inicioClase":["Este campo es obligatorio."]}}, status=400)
        
        if "meseSus" not in request.POST:
            if dia:
                dia = datetime.strptime(dia, "%Y-%m-%d")
                diaClase = dia.weekday()
                finClases =dia+timedelta(days=1)
                diasClases=[str(arreglarFormatoDia(dia=int(diaClase)))]
                horas = [copia["horaClase"]]
        else:
            meses = request.POST.get("meseSus")
            finClases = datetime.strptime(dia, "%Y-%m-%d")+relativedelta(months=int(meses))+timedelta(days=1)
            horas = json.loads(request.POST.get('horaClase'))
            diasClases = json.loads(request.POST.get('diaClase'))
        form = self.form_class(copia)
        if form.is_valid():
            profesor = form.cleaned_data["profesor"]
            horario = profesor.horarios
            horario = json.loads(horario)
            hora = [] 
            
            if horas == []: 
                return JsonResponse({"errores":{"Calendario":'Este campo es obligatorio','identificador':None}}, status=400)
            
            for i in range(len(horas)):
                if diasClases[0].replace('í', 'i') == 'Eliga un dia':
                    return JsonResponse({"errores":{"Calendario":'El día es un campo obligatorio','identificador':i}}, status=400)
                if horas[0] == '':
                    return JsonResponse({"errores":{"Calendario":'La hora es un campo obligatorio','identificador':i}}, status=400)
                hora.append(datetime.strptime(horas[i], '%H:%M').replace(minute = 0, second = 0))
                
            dias = [[str(i[1]) for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in diasClases]]][0]
            
            for i in range(len(hora)):
                diasNo = 'los días '+str(dias[i])+' a las '+hora[i].strftime('%I:%M %p')+' el profesor no esta disponible'
                if [hor for hor in [horary for horary in horario if horary['day'] in [dia for dia in dias]] if datetime.strptime(hor['from'], '%H:%M').time() <= hora[i].time() and (datetime.strptime(hor['through'], '%H:%M')-timedelta(hours=1)).time() >= hora[i].time()] == []:
                    if "meseSus"  in request.POST:
                        return JsonResponse({"errores":{"Calendario":diasNo,'identificador':i}}, status=400)
                    else:
                        return JsonResponse({"errores":{"profesor":diasNo,'identificador':None}}, status=400)
            # VALIDACIÓN PARA LOS PICADEORS 
            try:
                nivel = Nivel.objects.get(pk=copia["nivel"])
                picaderoNivel =  Picadero.objects.get(nivel=nivel)
            except:
                return JsonResponse({"errores":{"nivel":"No se puede agregar este estudiante porque no hay un picadero con el nivel seleccionado"}}, status=400)
            errores = [{},{}]
            max_estudiantes = picaderoNivel.max_estudiantes
            max_profes = picaderoNivel.max_profesores
            picaderos = InfoPicadero.objects.all()
            picaderos = picaderos.filter(dia__in = diasClases).filter(hora__in=hora).filter(picadero=picaderoNivel)
            profesor = Profesor.objects.get(pk=copia["profesor"])
            for picadero in picaderos:
                try:
                    iPicadero = picadero
                except:
                    iPicadero = ""
                    
                if iPicadero != "":
                    print(iPicadero)
                    # for profesor in profesores:
                    profesores = len(list(set([clases.clase.profesor for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)])))
                    estudiantes = len([clases.clase.calendario.registro for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)])
                    print(estudiantes, profesores, "\n----------------\n")
                    ElProfeEstaEnLaClase = profesor in [clases.clase.profesor for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)] 
                    if estudiantes >= max_estudiantes:
                        errores = serialiserValidation(errores, 0, iPicadero, 'estudiante')
                        
                    if ElProfeEstaEnLaClase:
                        if  profesores-1 >= max_profes:
                            errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
                    else:
                        if  profesores >= max_profes:
                            errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
            print(errores)                
            if errores!=[]:    
                if errores[0]!={}:
                    return JsonResponse({"errores":{"estudiante":[f"No puede asignar este {errores[0]['tipo']} porque el picadero: {errores[0]['contenido']['nombre']} los dias {errores[0]['contenido']['dias']} a las {errores[0]['contenido']['hora']} no admite más estudiantes"]}}, status=400)
                elif errores[1]!={}:
                    return JsonResponse({"errores":{"profesor":[f"No puede asignar este {errores[1]['tipo']} porque el picadero: {errores[1]['contenido']['nombre']} los dias {errores[1]['contenido']['dias']} a las {errores[1]['contenido']['hora']} no admite más profesores"]}}, status=400)
           
            # FIN VALIDACIÓN PARA LOS PICADEROS
            objecto = form.save()
            picadero = Picadero.objects.get(nivel = objecto.nivel)
            for i in range(len(hora)):
                calendario = CalendarioModel.objects.create(horaClase=hora[i],finClase=finClases,inicioClase=diaOriginal,diaClase = str(diasClases[i]), registro=objecto)
                calendario.save()
                clase =  Clase.objects.create(calendario=calendario, profesor=objecto.profesor)
                clase.save()
                iPicadero, creado = InfoPicadero.objects.get_or_create(picadero=picadero,hora=hora[i], dia=diasClases[i]) 
                iPicadero.save()
                iPicadero.clases.add(clase)
                # raise Exception("para que no me guarde gracias")
            return redirect('estudiantes') 
        else:
            return JsonResponse({"errores": form.errors}, status=400)
           

    def form_invalid(self, form):
        return JsonResponse({"errores": form.errors}, status=400)

class VerInfoEstudiante(IsAdminMixin, DetailView):
    model=Estudiante
    template_name = "Estudiantes/verInfoEstudiante.html"
    
    def get_context_data(self, **kwargs):
        contexto =  super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        registro = Registro.objects.get(estudiante=estudiante)
        calendario = CalendarioModel.objects.filter(registro=registro)
        contexto["registro"] = registro
        contexto['calendario']=calendario
        calendario = [[i for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in [dias.diaClase for dias in calendario]]]][0]
        contexto['diaClase']=calendario
        return contexto

class ModificarEstudiante(IsAdminMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "Estudiantes/editarInfoEstudiante.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        registro = Registro.objects.get(estudiante=estudiante)
        contexto["registro"] = registro
        contexto["formRegistro"] = RegistroForm(instance=registro)
        calendario = CalendarioModel.objects.filter(registro=registro)
        contexto['calendario']=calendario
        contexto['horas'] = [[i.strftime('%H:%M') for i in [hora.horaClase for hora in calendario]]][0]
        calendario = [[i for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in [dias.diaClase for dias in calendario]]]][0]
        contexto['diaClase']=calendario
        return contexto



class ModificarDocsEstudiante(IsAdminMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "Estudiantes/editarInfoEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def post(self, request, *args, **kwargs):
        estudiante = Estudiante.objects.get(pk=self.kwargs["pk"])
        acciones = []
        if request.FILES:
            if "documento_A" in request.FILES:
                estudiante.documento_A = request.FILES["documento_A"]
                messages.add_message(request, messages.INFO, "El documento de identidad ha sido modificado")
            if "seguro_A" in request.FILES:
                estudiante.seguro_A = request.FILES["seguro_A"]
                messages.add_message(request, messages.INFO, "El documento de la EPS ha sido modificado")
            if "firma" in request.FILES:
                estudiante.firma = request.FILES["firma"]
                messages.add_message(request, messages.INFO, "La firma ha sido modificada")
            estudiante.save()
        return redirect("modificarEstudiante",pk= self.kwargs["pk"])
   

class CambiarEstadoEstudiante(IsAdminMixin, View):
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

class ValidarRegistroEstudiante(IsAdminMixin, View):
    def post(self, request, *args, **kwargs):
        # dia = request.POST.get("dia")[2]
        # print(dia)
        # estudiante = request.POST.get("estudiante")
        # estudiante = Estudiante.objects.get(pk=estudiante)
        # registro = Registro.objects.get(estudiante=estudiante)
        # estudiantesDia = Registro.objects.filter(diaClase__icontains=dia)
        # estudiantesDia = Estudiante.objects.filter(pk__in = [x.id for x in estudiantesDia])
        # estudiantesDia = int(estudiantesDia.filter(nivel=estudiante.nivel.id).count())
        estudiantesDia=2
        return JsonResponse({"cant":estudiantesDia})

class ModificarRegistroEstudiante(IsAdminMixin, UpdateView):
    model = Registro
    form_class = RegistroForm
    template_name = "Estudiantes/editarInfoEstudiante.html"
    success_url = reverse_lazy("estudiantes")

    def post(self, request, *args, **kwargs):
        copia = request.POST.copy()
        dia = request.POST.get('inicioClase')
        diaOriginal = dia   
        if not dia:
            return JsonResponse({"errores":{"inicioClase":["Este campo es obligatorio."]}}, status=400)
        
        if "meseSus" not in request.POST:
            if dia:
                dia = datetime.strptime(dia, "%Y-%m-%d")
                diaClase = dia.weekday()
                finClases =dia+timedelta(days=1)
                diasClases=[str(arreglarFormatoDia(dia=int(diaClase)))]
                horas = [copia["horaClase"]]
                print("meses sus")
        else:
            meses = request.POST.get("meseSus")
            finClases = datetime.strptime(dia, "%Y-%m-%d")+relativedelta(months=int(meses))+timedelta(days=1)
            horas = json.loads(request.POST.get('horaClase'))
            diasClases = json.loads(request.POST.get('diaClase'))
            print("sin meses sus")
        get_object = Registro.objects.get(pk = kwargs['pk'])
        form = self.form_class(copia or None, instance=get_object)
        
        if form.is_valid():
            try:
                profesor = form.cleaned_data["profesor"]
                horario = profesor.horarios
                horario = json.loads(horario)
                hora = [] 
                
                if horas == []:
                    return JsonResponse({"errores":{"Calendario":'Este campo es obligatorio','identificador':None}}, status=400)
                for i in range(len(horas)):
                    if diasClases[0].replace('í', 'i') == 'Eliga un dia':
                        return JsonResponse({"errores":{"Calendario":'El día es un campo obligatorio','identificador':i}}, status=400)
                    if horas[0] == '':
                        return JsonResponse({"errores":{"Calendario":'La hora es un campo obligatorio','identificador':i}}, status=400)
                    hora.append(datetime.strptime(horas[i], '%H:%M').replace(minute = 0, second = 0))
                dias = [[str(i[1]) for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in diasClases]]][0]
                for i in range(len(hora)):
                    for i in range(len(dias)):
                        if dias[i] not in [horary['day'] for horary in horario]:
                            if "meseSus"  in request.POST:
                                return JsonResponse({"errores":{"Calendario":f'El profesor {profesor} no trabaja el dia {dias[i]}','identificador':i}}, status=400)
                            else:
                                return JsonResponse({"errores":{"profesor":f'El profesor {profesor} no trabaja el dia {dias[i]}','identificador':None}}, status=400)
                    diasNo = 'los días '+str(dias[i])+' a las '+hora[i].strftime('%I:%M %p')+' el profesor no esta disponible'
                    if [hor for hor in [horary for horary in horario if horary['day'] in [dia for dia in dias]] if datetime.strptime(hor['from'], '%H:%M').time() <= hora[i].time() and (datetime.strptime(hor['through'], '%H:%M')-timedelta(hours=1)).time() >= hora[i].time()] == []:
                        if "meseSus"  in request.POST:
                            return JsonResponse({"errores":{"Calendario":diasNo,'identificador':i}}, status=400)
                        else:
                            return JsonResponse({"errores":{"profesor":diasNo,'identificador':None}}, status=400)
                horarios = CalendarioModel.objects.filter(registro=get_object)
                for i in range(len(horarios)):
                    horarios[i].delete()
                objecto = form.save()   
                for i in range(len(hora)):
                    calendario = CalendarioModel.objects.create(horaClase=hora[i],finClase=finClases,inicioClase=diaOriginal,diaClase = str(diasClases[i]), registro=objecto)
                    calendario.save()
                return redirect('estudiantes')
            except Exception as error:
                print(error)
                if type(error).__name__ == "FormValidationEstudianteError":
                    return JsonResponse({"errores": {"estudiante":[str(error)]}}, status=400)
                elif type(error).__name__ == "FormValidationProfesorError":
                    print("tengo algun error aqui")
                    return JsonResponse({"errores": {"profesor":[str(error)]}}, status=400)
                elif type(error).__name__ == "FormValidationNiveleError":
                    return JsonResponse({"errores": {"nivel":[str(error)]}}, status=400)
            
        else:
            return JsonResponse({"errores": form.errors}, status=400)
        return JsonResponse({"mensaje":"estudiante modificado con exito"}, status=400)
        return redirect('estudiantes')
