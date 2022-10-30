from datetime import datetime, timedelta, date
from time import time
from django.shortcuts import render, redirect
from django.views.generic import View,  DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

from Picaderos.models import EstadoClase, Picadero
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
    model=CalendarioModel
    template_name = "Calendario/verInfoEstudianteCalendario.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        registro = self.get_object()
        clases = Asistencia.objects.filter(registro=registro.registro)
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
        clasesHoy = list(clasesHoy)
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
                            claseObject.save()
                            messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha pasado a la lista de clases canceladas correctamente")
                        else:
                            claseObject.estado = True
                            # objecto.objects.filter(dia='martes').filter(estado=False).count()x
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

