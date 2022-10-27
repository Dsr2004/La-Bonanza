import json
import pandas as pd
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from io import BytesIO
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q
from Usuarios.models import Usuario
from La_Bonanza. mixins import IsAdminMixin
from Niveles.models import Nivel
from Picaderos.models import Picadero, InfoPicadero, Clase
from .models import Estudiante, Registro, Profesor, Asistencia, Calendario as CalendarioModel
from .forms import EstudianteForm,CrearEstudianteForm, RegistroForm,ProfesorForm
from .models import DIAS_SEMANA



def arreglarFormatoDia(dia):
    if type(dia)  != list:
        if str(dia) == "6":
            dia = 0 #en las variables del modelo el domingo es 0 porque asi lo recibe fullcalendar pero python retorna el domingo como 6
        else:
            dia = dia+1
        return dia
    else:
        dias = []
        for dia in dia:
            if str(dia) == "6":
                dias.append(0) #en las variables del modelo el domingo es 0 porque asi lo recibe fullcalendar pero python retorna el domingo como 6
            else:
                dias.append(int(dia)+1)
        return dias
    
def serialiserValidation(lista, i, iPicadero, tipo):
    errores = list(lista)
    if errores!=[]:
        if errores[i]!={}:
            nombre = errores[i]['contenido']['nombre']
            dias = errores[i]['contenido']['dias']
            horas = errores[i]['contenido']['hora']
            print(dias)
            print(horas)
            if iPicadero.get_dia_display() not in errores[i]['contenido']['dias'].split(', '):
                dias = errores[i]['contenido']['dias'].split(', ')
                dias.append(iPicadero.get_dia_display())
                dias = ', '.join(list(reversed(dias)))
            errores[i] = {"tipo":tipo,'contenido':{'nombre':nombre,'dias':dias,'hora':horas}}
        else:
            errores[i] = {"tipo":tipo,'contenido':{'nombre':iPicadero.picadero.nombre,'dias':iPicadero.get_dia_display(),'hora':iPicadero.hora.strftime('%I:%M %p')}}
    return errores

class Calendario(View):
    template_name = "calendario.html"
    model = CalendarioModel
    def get(self, request, *args, **kwargs):
        estudiantes = Estudiante.objects.filter(estado=True)
        registros = []
        if estudiantes:
            if request.user.administrador:
                calendarios = CalendarioModel.objects.all()
                for calendario in calendarios:
                    if calendario.registro.estudiante.estado==True:
                        registros.append(calendario)
            else:
                registros = Registro.objects.filter(estudiante__in=[x.pk for x in estudiantes]).filter(profesor=request.user.pk)
        ctx = {"clases":registros}
        print(ctx["clases"])
        return render(request, self.template_name ,ctx)

class VerInfoEstudianteCalendario(DetailView):
    model=Registro
    template_name = "Calendario/verInfoEstudianteCalendario.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        registro = self.get_object()
        clases = Asistencia.objects.filter(registro=registro)
        conteoClases = clases.count()
        conteoClaesAsistidas = clases.filter(estado=1).count()
        conteoClaesNoAsistidas = clases.filter(estado=2).count()
        conteoClaesCanceladas = clases.filter(Q(estado=3)|Q(estado=4)).count()
        ctx["totalClases"]=conteoClases
        ctx["AsitidasClases"]=conteoClaesAsistidas
        ctx["NoAsistidasClases"]=conteoClaesNoAsistidas
        ctx["CanceladasClases"]=conteoClaesCanceladas
        return ctx


class GestionDeAsistencia(View):
    template_name = "asistencia.html"
    model = Registro
    def get(self, request, *args, **kwargs):
        ctx = {}
        hoy = datetime.now()
        hoyA = date.today()
        diaSemana = arreglarFormatoDia(hoy.weekday())
        estudiantes = Estudiante.objects.filter(estado=True)
        if request.user.administrador:
            clasesHoy = Registro.objects.filter(diaClase__icontains=diaSemana).filter(estudiante__in=[x.pk for x in estudiantes]).order_by("horaClase")
        else:
            clasesHoy = Registro.objects.filter(diaClase__icontains=diaSemana).filter(estudiante__in=[x.pk for x in estudiantes]).order_by("horaClase").filter(profesor=request.user.pk)
        clasesHoy = list(clasesHoy)
        clasesHoyRango = []
        for clases in clasesHoy:
            if clases.inicioClase  <= hoyA <= clases.finClase:
                clasesHoyRango.append(clases)
             
        
        ctx["dia"]=hoy.date()
        ctx["hora"]=hoy.time()
        ctx["clases"]=clasesHoyRango
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
                asistencia, creado = Asistencia.objects.get_or_create(registro=registro, dia=datetime.now().date(), hora=hora, nivel=registro.nivel) 
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
        ctx = {"dia":dia}
        if request.user.administrador:
            asistencia = self.model.objects.filter(dia=dia).order_by("hora")
            ctx["asistencia"]=asistencia
        else:
            asistencia = self.model.objects.filter(dia=dia).order_by("hora")
            asistenciaValida = [i for i in [x for x in asistencia if x.registro.profesor is not None] if i.registro.profesor.pk == request.user.pk]
            ctx["asistencia"]=asistenciaValida
       
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
                    clases = iPicadero.clases.all()
                    profesores = clases.values_list("profesor").distinct().count()
                    estudiantes = clases.values_list("estudiante").distinct().count()
                    print(estudiantes, profesores, "\n----------------\n")
                    ElProfeEstaEnLaClase = clases.filter(profesor=profesor).distinct()
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
            raise Exception("para que no me guarde gracias")
            objecto = form.save()
            for i in range(len(hora)):
                calendario = CalendarioModel.objects.create(horaClase=hora[i],finClase=finClases,inicioClase=diaOriginal,diaClase = str(diasClases[i]), registro=objecto)
                calendario.save()
                print(calendario)
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
        contexto["registro"] = registro
        return contexto

class ModificarEstudiante(IsAdminMixin, UpdateView):
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
        print(form.errors)
        return JsonResponse({"errores": form.errors}, status=404)


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
        if "meseSus" not in request.POST:
            dia = request.POST.get('inicioClase')
            dia = datetime.strptime(dia, "%Y-%m-%d")
            diaClase = dia.weekday()
            copia["finClase"]=dia+relativedelta(days=1)
            copia["diaClase"]=arreglarFormatoDia(dia=int(diaClase))
        else:
            meses = request.POST.get("meseSus")
            dia = request.POST.get('inicioClase') 
            finClases = datetime.strptime(dia, "%Y-%m-%d")+relativedelta(months=int(meses))
            copia["finClase"]=finClases
        form = self.form_class(copia, instance=self.get_object())
        if form.is_valid():
            form.save()
            return JsonResponse({"mensaje":"guardado correctamente"}, status=200)
        else:
            return JsonResponse({"errores": form.errors}, status=400)

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
            dias = []
            try:
                horarios = json.loads(profe.horarios)
                for horas in horarios:
                    desde = datetime.strptime(horas['from'], '%H:%M').strftime('%I:%M %p')
                    hasta=datetime.strptime(horas['through'], '%H:%M').strftime('%I:%M %p')
                    dias.append(horas['day'])
                    horario.append('De '+str(desde)+' Hasta '+str(hasta))
            except:
                horario.append('Este profesor no tiene horario')
            horario = str(horario).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            dias = str(dias).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            diccionario = {'horarios':horario.split(' - '), 'dias':dias.split(' - ')}
            horario=[]
            for i in range(len(diccionario['horarios'])):
                horario.append('Para el día '+diccionario['dias'][i] + ' el horario es '+diccionario['horarios'][i])
            datos.append({'profesor':profe, 'horario':horario})
            contexto['Profesor'] = datos[0]
            contexto['Registros'] = Registro.objects.filter(profesor = profe)
            return render(request, self.template_name, contexto)
        contexto={}
        datos=[]
        for profe in Profesor.objects.all():
            horario = []
            dias = []
            try:
                horarios = json.loads(profe.horarios)
                for horas in horarios:
                    desde = datetime.strptime(horas['from'], '%H:%M').strftime('%I:%M %p')
                    hasta=datetime.strptime(horas['through'], '%H:%M').strftime('%I:%M %p')
                    dias.append(horas['day'])
                    horario.append('Desde '+str(desde)+' Hasta '+str(hasta))
            except:
                horario.append('Este profesor no tiene horario')
            horario = str(horario).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            dias = str(dias).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            datos.append({'profesor':profe, 'horario':horario,'dias':dias})
        contexto['Profesores'] = datos
        return render(request, self.template_name, contexto)

class infoProfesor(ListView):
    template_name = "Profesores/verInfoProfesor.html"
    model = Profesor
    
    def get(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        contexto={}
        datos=[]
        for profe in Profesor.objects.filter(id=kwargs['pk']):
            horario = []
            dias = []
            try:
                horarios = json.loads(profe.horarios)
                for horas in horarios:
                    desde = datetime.strptime(horas['from'], '%H:%M').strftime('%I:%M %p')
                    hasta=datetime.strptime(horas['through'], '%H:%M').strftime('%I:%M %p')
                    dias.append(horas['day'])
                    horario.append('De '+str(desde)+' Hasta '+str(hasta))
            except:
                horario.append('Este profesor no tiene horario')
            horario = str(horario).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            dias = str(dias).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            diccionario = {'horarios':horario.split(' - '), 'dias':dias.split(' - ')}
            horario=[]
            for i in range(len(diccionario['horarios'])):
                horario.append('Para el día '+diccionario['dias'][i] + ' el horario es '+diccionario['horarios'][i])
            datos.append({'profesor':profe, 'horario':horario})
        contexto['Profesor'] = datos
        return render(request, self.template_name, contexto)

class editProfesor(IsAdminMixin, TemplateView):
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
            dias = []
            try:
                horarios = json.loads(profe.horarios)
                for horas in horarios:
                    desde = datetime.strptime(horas['from'], '%H:%M').strftime('%I:%M %p')
                    hasta=datetime.strptime(horas['through'], '%H:%M').strftime('%I:%M %p')
                    dias.append(horas['day'])
                    horario.append('Desde '+str(desde)+' Hasta '+str(hasta))
            except:
                horario.append('Este profesor no tiene horario')
            horario = str(horario).replace("'", '').replace("[", '').replace("]", '').replace(',', ' -')
            datos.append({'profesor':profe, 'horarios':horario.split(', '), 'dias':dias})
        contexto['Profesor'] = datos[0]
        contexto['horarios'] = json.loads(datos[0]['profesor'].horarios)
        contexto['horarios'] = json.dumps(contexto['horarios'])
        contexto['dias'] = json.dumps(datos[0]['dias'])
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


class ConteoClasesFecha(View):
    def post(self,request, *args, **kwargs):
        fechas = request.POST.get("fechas").split(" - ")
        fechas=[datetime.strptime(fechas[0], '%m/%d/%Y').date(), datetime.strptime(fechas[1], '%m/%d/%Y').date()]
        id = self.kwargs["pk"]
        registro = Registro.objects.get(pk=id)
        clases = Asistencia.objects.filter(registro=registro)
        conteoClases=0
        conteoClaesAsistidas=0
        conteoClaesNoAsistidas=0
        conteoClaesCanceladas=0
        for clase in clases:
            if clase.dia <= fechas[1] and clase.dia >= fechas[0]:
                print(clase.dia)
                conteoClases +=1
                if clase.estado=="1":
                    conteoClaesAsistidas+=1
                elif clase.estado == "2":
                    conteoClaesNoAsistidas+=1
                elif clase.estado == "3" or clase.estado == "4":
                    conteoClaesCanceladas +=1
        ctx = {}
        ctx["totalClases"]=conteoClases
        ctx["AsitidasClases"]=conteoClaesAsistidas
        ctx["NoAsistidasClases"]=conteoClaesNoAsistidas
        ctx["CanceladasClases"]=conteoClaesCanceladas
        return JsonResponse(ctx, status=200)