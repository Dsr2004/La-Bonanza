import json
from datetime import datetime, timedelta, date
from time import time
from django.shortcuts import render, redirect
from django.views.generic import View,  DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from Picaderos.models import EstadoClase, InfoPicadero, Picadero, EstadoClase
from Niveles.models import Nivel
from ..models import DIAS_SEMANA, Estudiante, Registro, Profesor, Asistencia, Calendario as CalendarioModel

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
    model = EstadoClase
    def get(self, request, *args, **kwargs):
        registros = []
        estadoClase = EstadoClase.objects.filter(estado = True)
        if request.user.administrador:
            for clases in estadoClase:
                calendario = clases.clase.calendario
                if calendario.registro.estudiante.estado==True:
                    registros.append(clases)
        else:
             for clases in estadoClase:
                calendario = clases.clase.calendario
                if calendario.registro.profesor == request.user.pk:
                    if calendario.registro.estudiante.estado==True:
                        registros.append(clases)
        ctx = {"clases":list(set(registros))}
        
        print(ctx["clases"])
        return render(request, self.template_name ,ctx)

class VerInfoEstudianteCalendario(DetailView):
    model=EstadoClase
    template_name = "Calendario/verInfoEstudianteCalendario.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        registro = self.get_object().clase.calendario.registro
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
    
class ConteoClasesFecha(View):
    def post(self,request, *args, **kwargs):
        fechas = request.POST.get("fechas").split(" - ")
        fechas=[datetime.strptime(fechas[0], '%m/%d/%Y').date(), datetime.strptime(fechas[1], '%m/%d/%Y').date()]
        id = self.kwargs["pk"]
        clase = EstadoClase.objects.get(pk=id)
        registro = clase.clase.calendario.registro
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

class GestionDeAsistencia(View):
    template_name = "asistencia.html"
    model = CalendarioModel
    def get(self, request, *args, **kwargs):
        ctx = {}
        hoy = datetime.now()
        hoyA = date.today()
        diaSemana = arreglarFormatoDia(hoy.weekday())
        
        clasesHoy = self.model.objects.filter(diaClase = diaSemana)
        clasesHoy = clasesHoy.filter(registro__in = [x.registro.pk  for x in clasesHoy if x.registro.estudiante.estado == True]).order_by("horaClase")
        if not request.user.administrador:
            clasesHoy = clasesHoy.filter(registro__in=[x.registro.pk for x in clasesHoy if x.registro.profesor.pk == request.user.pk ]).order_by("horaClase")
        clasesHoy = [clases.clase.calendario for clases in EstadoClase.objects.all() if clases.clase.calendario in clasesHoy and clases.estado != False]
        clasesHoy = list(set(clasesHoy))
        clasesHoyRango = []
        for clases in clasesHoy:
            if clases.inicioClase  <= hoyA <= clases.finClase:
                clasesHoyRango.append(clases)
          
        
        ctx["dia"]=hoy.date()
        ctx["hora"]=hoy.time()
        ctx["clases"]=clasesHoyRango
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
        for clase in clasesDia:
            try:
                hoy = datetime.now()
                diaSemana = arreglarFormatoDia(hoy.weekday())
                registro = Registro.objects.get(estudiante=clase["estudiante"])
                picadero = Picadero.objects.get(nivel=registro.nivel)
                asistencia, creado = Asistencia.objects.get_or_create(registro=registro, dia=datetime.now().date(), hora=hora, picadero=picadero)
                calendario = CalendarioModel.objects.filter(registro=registro)
                calendario = [objecto for objecto in calendario if int([dia[0] for dia in DIAS_SEMANA if int(dia[0]) == int(objecto.diaClase)][0]) == int(diaSemana) and objecto.horaClase == hora][0]
                claseObject = [clases for clases in EstadoClase.objects.all() if clases.clase.calendario == calendario][0]
                print(claseObject)
                if creado:
                    asistencia.estado = clase["estado"]
                    asistencia.save()
                    messages.add_message(request, messages.INFO, f"{registro.estudiante.nombre_completo} ha sido registrado correctamente en la asistencia del día")
                else:
                    if asistencia.estado != clase["estado"]:
                        if clase['estado'] == '3' or clase['estado'] == '4':
                            claseObject.estado = False
                            claseObject.fecha_cancelacion = datetime.now().time()
                            claseObject.save()
                            messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha pasado a la lista de clases canceladas correctamente")
                        else:
                            claseObject.estado = True
                            claseObject.save()
                        asistencia.estado=clase["estado"]
                        asistencia.save()
                        messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha sido modificado, porque ya estaba en la asistencia del día")
            except  Exception as e:
                print(e)
                messages.add_message(request, messages.INFO, f"No se encontro al estudiante en la base de datos")
        
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

class ClasesCanceladas(View):
    def get(self, request, *args, **kwargs):
        clases = EstadoClase.objects.filter(estado=False)
        clasesV = []
        hoy = datetime.now().date()
        for clase in clases:
            if len([d for d in clasesV if d['fecha'] == clase.fecha_cancelacion]) > 0:
                indice = clasesV.index([d for d in clasesV if d['fecha'] == clase.fecha_cancelacion][0])
                clasesV[indice]['clases'].append(clase)
            else:
                if (hoy-clase.fecha_cancelacion).days+1 >= 0 and (hoy-clase.fecha_cancelacion).days+1 <= 22:
                    clasesV.append({'fecha':clase.fecha_cancelacion,'clases':[clase],'validacion':True})
                else:
                    clasesV.append({'fecha':clase.fecha_cancelacion,'clases':[clase], 'validacion':False})
        ctx = {"clases":clasesV}
        return render(request, "clasesCanceladas.html",ctx)
    
    
class ReponerClase(View):
    def get(self, request, *args, **kwargs):
        clase = EstadoClase.objects.get(pk=self.kwargs["pk"])
        return render(request, "Clases/editarClaseCancelada.html",{"clase":clase})
    def post(self, request, *args, **kwargs):
        if request.POST.get('tipo') == 'consultaProfesor':
            clase = EstadoClase.objects.get(pk = kwargs['pk'])
            profesores = [profesor.pk for profesor in Profesor.objects.all() if clase.InfoPicadero.picadero.nivel in profesor.niveles.all() and profesor.usuario.estado == True]
            calendario = clase.clase.calendario
            data = {'Profesores':{'profesoresPk':profesores,'profesoresName': [profesor.usuario.nombres for profesor in Profesor.objects.all() if clase.InfoPicadero.picadero.nivel in profesor.niveles.all() and profesor.usuario.estado == True]}, 'ActualProfesor':{'ProfesorPk':clase.clase.profesor.pk,'ProfesorName':clase.clase.profesor.usuario.nombres}}
            return JsonResponse(data, status=200)
        elif  request.POST.get('tipo') == 'editar':
            dia = request.POST.get("dia")
            hora =request.POST.get("hora")
            profesor = request.POST.get("profesor")
            
            errores = {}
            if not dia:
                errores["dia"]="Este campo es obligatorio."
            if not hora:
                errores["dia"]="Este campo es obligatorio."
            if not profesor:
                errores["dia"]="Este campo es obligatorio."
            if errores:
                return JsonResponse({"errores":errores}, status=400)
            dia = datetime.strptime(dia, "%Y-%m-%d")
            hora = datetime.strptime(hora, "%H:%M")
            profesor = Profesor.objects.get(pk=profesor)
            horario = profesor.horarios
            horario = json.loads(horario)
            clase = EstadoClase.objects.get(pk = kwargs['pk'])
            # validacion de disponibilidad de profesores 
            dias = [[str(i[1]) for i in [dia for dia in DIAS_SEMANA] if int(i[0]) == arreglarFormatoDia(dia.weekday())]][0]
            diasNo = 'los días '+str(dias[0])+' a las '+hora.strftime('%I:%M %p')+' el profesor no esta disponible'
            if [hor for hor in [horary for horary in horario if horary['day'] in [dia for dia in dias]] if datetime.strptime(hor['from'], '%H:%M').time() <= hora.time() and (datetime.strptime(hor['through'], '%H:%M')-timedelta(hours=1)).time() >= hora.time()] == []:
                if "meseSus"  in request.POST:
                    return JsonResponse({"errores":{"Calendario":diasNo,'identificador':1}}, status=400)
                else:
                    return JsonResponse({"errores":{"profesor":diasNo,'identificador':None}}, status=400)

             # VALIDACIÓN PARA LOS PICADEORS 
            try:
                picadero =  clase.InfoPicadero.picadero
            except:
                return JsonResponse({"errores":{"nivel":"No se puede agregar este estudiante porque no hay un picadero con el nivel seleccionado"}}, status=400)
            errores = [{},{}]
            max_estudiantes = picadero.max_estudiantes
            max_profes = picadero.max_profesores
            picaderos = InfoPicadero.objects.all()
            picaderos = picaderos.filter(dia = arreglarFormatoDia(dia.weekday())).filter(hora=hora).filter(picadero=picadero)
            for picadero in picaderos:
                try:
                    iPicadero = picadero
                except:
                    iPicadero = ""
                if iPicadero != "":
                    profesores = len(list(set([clases.clase.profesor for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)])))
                    estudiantes = len(list(set([clases.clase.calendario.registro for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)])))
                    ElProfeEstaEnLaClase = profesor in [clases.clase.profesor for clases in EstadoClase.objects.filter(InfoPicadero=iPicadero)] 
                    if estudiantes >= max_estudiantes:
                        errores = serialiserValidation(errores, 0, iPicadero, 'estudiante')
                    claseSelected = [diasC for diasC in EstadoClase.objects.all() if dia.date() == diasC.dia and hora.time() == diasC.clase.calendario.horaClase]
                    print(dia.date() in [diasC.dia for diasC in EstadoClase.objects.all() if  hora.time() == diasC.clase.calendario.horaClase])
                    if len(claseSelected)>0:
                        Clases = [pro.clases.all() for pro in InfoPicadero.objects.filter(picadero=clase.InfoPicadero.picadero) if int(pro.dia) == arreglarFormatoDia(dia.weekday()) and pro.hora == hora.time()]
                        for pforsor in [clase[0].profesor for clase in Clases]:
                            if profesor != pforsor:
                                if ElProfeEstaEnLaClase:
                                    if  profesores-1 >= max_profes+1:
                                        errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
                                else:
                                    if  profesores >= max_profes:
                                        errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
                            else:
                                if ElProfeEstaEnLaClase:
                                    if  profesores-1 >= max_profes+1:
                                        errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
                                else:
                                    if  profesores >= max_profes+1:
                                        errores = serialiserValidation(errores, 1, iPicadero, 'profesor al estudiante')
                    else:
                        return JsonResponse({"errores":{"errores":"No hay clases este dia como sera posible editar algo inexistente?"}}, status=400)
                        
            print(errores)
            if errores!=[]:    
                if errores[0]!={}:
                    return JsonResponse({"errores":{"estudiante":[f"No puede asignar este {errores[0]['tipo']} porque el picadero: {errores[0]['contenido']['nombre']} los dias {errores[0]['contenido']['dias']} a las {errores[0]['contenido']['hora']} no admite más estudiantes"]}}, status=400)
                elif errores[1]!={}:
                    return JsonResponse({"errores":{"profesor":[f"No puede asignar este {errores[1]['tipo']} porque el picadero: {errores[1]['contenido']['nombre']} los dias {errores[1]['contenido']['dias']} a las {errores[1]['contenido']['hora']} no admite más profesores"]}}, status=400)
           
            # FIN VALIDACIÓN PARA LOS PICADEROS
            
            return JsonResponse({'dh':request.POST}, status=200)
            