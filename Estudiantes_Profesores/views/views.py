import json
from io import BytesIO
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time
from django.shortcuts import render, redirect
from django.views.generic import View,  DetailView
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q
from Usuarios.models import Usuario
from Picaderos.models import EstadoClase, InfoPicadero, Picadero, EstadoClase
from Niveles.models import Nivel
from Niveles.forms import NivelForm
from Usuarios.forms import UsuarioForm
from Estudiantes_Profesores.forms import EstudianteForm, ProfesorForm

from ..models import DIAS_SEMANA, Estudiante, Registro, Profesor, Asistencia, Calendario as CalendarioModel
from .validacion import ValidationClass
import time
import pandas as pd
import inspect
from La_Bonanza.settings import BASE_DIR
import os

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
        inicio = datetime.today().replace(day=1)
        if request.GET.get("fecha"):
            inicio = request.GET.get("fecha")
            
            inicio = datetime.strptime(inicio, "%m/%d/%Y")
        registros = []
        fin = inicio+relativedelta(months=1)
        
        estadoClase = EstadoClase.objects.filter(estado = True)
        estadoClase = [x for x in estadoClase if x.dia >= inicio.date() and x.dia<fin.date() ]
        if request.user.administrador:
            print("es un admin")
            for clases in estadoClase:
                calendario = clases.clase.calendario
                if calendario.registro.estudiante.estado==True:
                    
                    registros.append(clases)
        else:
            for clases in estadoClase:
                calendario = clases.clase.calendario
                print(calendario, calendario.registro.profesor)
                if calendario.registro.profesor:
                    if calendario.registro.profesor.pk == request.user.pk:
                        print("es un profe")
                        if calendario.registro.estudiante.estado==True:
                            registros.append(clases)
        ctx = {"clases":list(set(registros)),'cancelada':EstadoClase.objects.filter(estado = False).count(), "fecha":inicio}
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
        clasesHoy = [clases for clases in EstadoClase.objects.all() if clases.clase.calendario in clasesHoy and clases.estado == True]
        clasesHoy = [calendario for calendario in clasesHoy if calendario.dia == datetime.now().date()]
        clasesHoyRango = []
        for clases in clasesHoy:
            if clases.clase.calendario.inicioClase  <= hoyA <= clases.clase.calendario.finClase:
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
                calendario = CalendarioModel.objects.filter(registro=registro, inicioClase=hoy)
                calendario = [objecto for objecto in calendario if int([dia[0] for dia in DIAS_SEMANA if int(dia[0]) == int(objecto.diaClase)][0]) == int(diaSemana) and objecto.horaClase == hora][0]
                claseObject = [clases for clases in EstadoClase.objects.all() if clases.clase.calendario == calendario][0]
                if creado:
                    if clase['estado'] == '3' or clase['estado'] == '4':
                        print("fue creado",claseObject.estado)
                        asistencia.estado = clase["estado"]
                        asistencia.save()
                        claseObject.estado = False
                        claseObject.fecha_cancelacion = datetime.now().date()
                        claseObject.save()
                        messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha pasado a la lista de clases canceladas correctamente")
                    else:
                        asistencia.estado = clase["estado"]
                        asistencia.save()
                        messages.add_message(request, messages.INFO, f"{registro.estudiante.nombre_completo} ha sido registrado correctamente en la asistencia del día")
                else:
                    print("modificasdo",claseObject.estado)
                    if asistencia.estado != clase["estado"]:
                        if clase['estado'] == '3' or clase['estado'] == '4':
                            claseObject.estado = False
                            claseObject.fecha_cancelacion = datetime.now().date()
                            claseObject.save()
                            messages.add_message(request, messages.WARNING, f"{registro.estudiante.nombre_completo} ha pasado a la lista de clases canceladas correctamente")
                        else:
                            claseObject.estado = True
                            claseObject.save()
                        asistencia.estado=clase["estado"]
                        asistencia.save()
                        print(claseObject)
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
            if clase.fecha_cancelacion:
                if len([d for d in clasesV if d['fecha'] == clase.fecha_cancelacion]) > 0:
                    indice = clasesV.index([d for d in clasesV if d['fecha'] == clase.fecha_cancelacion][0])
                    clasesV[indice]['clases'].append(clase)
                else:
                    if (clase.fecha_cancelacion-hoy).days+1 >= 0 and (clase.fecha_cancelacion-hoy).days+1 <= 36:
                        clasesV.append({'fecha':clase.fecha_cancelacion,'clases':[clase],'validacion':True})
                    else:
                        clasesV.append({'fecha':clase.fecha_cancelacion,'clases':[clase], 'validacion':False})
        ctx = {"clases":clasesV}
        return render(request, "clasesCanceladas.html",ctx)
    
    
class ReponerClase(View):
    def get(self, request, *args, **kwargs):
        clase = EstadoClase.objects.get(pk=self.kwargs["pk"])
        profesores = [profesor for profesor in Profesor.objects.all() if profesor.usuario.estado == True]
        profeActual = clase.clase.profesor
        return render(request, "Clases/editarClaseCancelada.html",{"clase":clase, "profesores":profesores, "profeActual":profeActual})
    
    def post(self, request, *args, **kwargs):
        dia = request.POST.get("dia")
        hora =request.POST.get("hora")
        profesor = request.POST.get("profesor")
        errores = {}
        if not dia:
            errores["dia"]=["Este campo es obligatorio."]
        if not hora:
            errores["hora"]=["Este campo es obligatorio."]
        if not profesor:
            errores["profesor"]=["Este campo es obligatorio."]
        if errores:
            return JsonResponse({"errores":errores}, status=400)
        dia = datetime.strptime(dia, "%Y-%m-%d")
        
        numeroDia = arreglarFormatoDia(dia.weekday())
        try:
            hora = datetime.strptime(hora, "%H:%M:%S")
        except:
            hora = datetime.strptime(hora, "%H:%M")
            
        profesor = Profesor.objects.get(pk=profesor)
        validacion = ValidationClass()
        diasNo = validacion.HorarioProfesor(profesor=profesor, dia=numeroDia, hora=hora)
        
        if diasNo:
             return JsonResponse({"errores":{"profesor":diasNo,'identificador':None}}, status=400)

        error = validacion.ValidacionPicadero(profesor=profesor, dia=numeroDia, hora=hora, clasepk=kwargs["pk"], estado="BUSCAR")
        if error["tipo"] != "NO":
            if error["tipo"] == "estudiante":
                return JsonResponse({"errores":error["errores"]}, status=400)
            elif error["tipo"] == "profesor":
                return JsonResponse({"errores":error["errores"]}, status=400)
        clase = EstadoClase.objects.get(pk=kwargs["pk"])
        clase.dia = dia
        clase.fecha_cancelacion = None
        clase.estado = True
        Ipicadero = [newInfoPicadero for newInfoPicadero in InfoPicadero.objects.all() if int(newInfoPicadero.dia) == arreglarFormatoDia(dia.weekday()) and newInfoPicadero.hora == hora.time()]
        if Ipicadero == []:
            infoP = InfoPicadero.objects.create(picadero = clase.InfoPicadero.picadero, dia = arreglarFormatoDia(dia.weekday()), hora=hora.time())
            infoP.save()
            clase.save()
            EstadoClase.objects.create(InfoPicadero=infoP, clase=clase.clase, dia=clase.dia, estado=clase.estado, fecha_cancelacion=clase.fecha_cancelacion)
            clase.delete()
        else:
            clase.InfoPicadero = Ipicadero[0]
            clase.save()
        return redirect('clasesCanceladas')
            
class CargasMasivas(View):
    template_name = 'cargasMasivas.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)     
    def create_niveles(self, excel):
        message = []
        datos = [{d:[c for c in excel[d]]} for d in excel.columns if 'Unnamed' not in d]
        serializers = []
        registrados = int()
        for dato in datos:
            key = list(dato.keys())[0]
            for i, d in enumerate(dato[key]):
                if str(d) == 'nan':
                    d = ''
                try:
                    serializers[i][key] = d
                except:
                    serializers.insert(i, {key:d})
        for i, serialize in enumerate(serializers):
            form = NivelForm(serialize)
            if form.is_valid():
                form.save()
                registrados = registrados + 1
            else:
                mensaje = json.loads(form.errors.as_json())[list(form.errors.as_data().keys())[0]][0]['message']
                message.append(f'En la fila {i+2} "{list(form.errors.as_data().keys())[0]}" {mensaje}')
        
        if registrados:
            message.append(f'Se registraron {registrados} niveles en esta carga.')
        return message
    def create_instructores(self, excel):
        message = []
        try:
            datos = [{d:[c for c in excel[d]]} for d in excel.columns if 'Unnamed' not in d]
            serializers = []
            registrados = int()
            for dato in datos:
                key = list(dato.keys())[0]
                for i, d in enumerate(dato[key]):
                    if str(d) == 'nan':
                        d = ''
                    try:
                        serializers[i][key] = d
                    except:
                        serializers.insert(i, {key:d})
            for i, serialize in enumerate(serializers):
                form = UsuarioForm(serialize)
                formP = ProfesorForm(serialize)
                if form.is_valid():
                    if formP.is_valid():
                        registrados = registrados + 1
                        print('si')
                    else:
                        mensaje = json.loads(formP.errors.as_json())[list(formP.errors.as_data().keys())[0]][0]['message']
                        message.append(f'En la fila {i+2} "{list(formP.errors.as_data().keys())[0]}" {mensaje}')
                else:
                    mensaje = json.loads(form.errors.as_json())[list(form.errors.as_data().keys())[0]][0]['message']
                    message.append(f'En la fila {i+2} "{list(form.errors.as_data().keys())[0]}" {mensaje}')
            
            if registrados:
                message.append(f'Se registraron {registrados} instructores en esta carga.')
        except Exception as e:
            print('exc', e)
        return message
    
    def post(self, request, *args, **kwargs):
        context = {}
        if 'niveles' in request.FILES:
            try:
                io = request.FILES['niveles'].read()
                excel = pd.read_excel(io)
                attributes = inspect.getmembers(Nivel, lambda a:not(inspect.isroutine(a)))
                attributes = [a for a in attributes if a[0] == '__doc__'][0][1].replace('Nivel', '').replace('(','').replace(')', '').split(', ')
                campos = list(filter(lambda attr: attr != 'id', attributes))
                if len([c for c in campos if c in excel.columns]) == len(campos):
                    context = {'errors':{'niveles':self.create_niveles(excel)}}
                else:
                    context = {'errors':{'niveles':['Los campos necesarios para realizar la carga no se encuentran en el excel cargado. Se recomienda seguir el formato de la plantilla.']}}
                    
            except Exception as e:
                print('Exception:',e)
                context = {'errors':{'niveles':['Extensión '+(str(request.FILES['niveles']).split('.')[-1]).upper()+' no permitida solo se admiten Excels.']}}
        elif 'instructores' in request.FILES:
            try:
                io = request.FILES['instructores'].read()
                excel = pd.read_excel(io)
                campos = ['usuario','nombres','celular','apellidos','cedula','fecha_nacimiento','email','horarios']
                if len([c for c in campos if c in excel.columns]) == len(campos):
                    context = {'errors':{'instructores':self.create_instructores(excel)}}
                else:
                    context = {'errors':{'instructores':['Los campos necesarios para realizar la carga no se encuentran en el excel cargado. Se recomienda seguir el formato de la plantilla.']}}
            except Exception as e:
                print(e)
                context = {'errors':{'instructores':['Extensión '+(str(request.FILES['instructores']).split('.')[-1]).upper()+' no permitida solo se admiten Excels.']}}
        elif 'alumnos' in request.FILES:
            io = request.FILES['alumnos'].read()
            excel = pd.read_excel(io)
            attributes = inspect.getmembers(Estudiante, lambda a:not(inspect.isroutine(a)))
            attributes = [a for a in attributes if a[0] == '__doc__'][0][1].replace('Estudiante', '').replace('(','').replace(')', '').split(', ')
            campos = list(filter(lambda attr: attr != 'id' and attr != 'firma' and attr != 'nombrefirma' and attr != 'estado' and attr != 'aceptaContrato' and attr != 'autorizaClub' and attr != 'exoneracion' and attr != 'documento_A' and attr != 'seguro_A' and attr != 'imagen' and attr != 'nombre_completo' and attr != 'comprobante_documento_identidad' and attr != 'comprobante_seguro_medico', attributes))
            print(campos)
            if len([c for c in campos if c in excel.columns]) == len(campos):
                pass
            else:
                context = {'errors':{'niveles':'Los campos necesarios para realizar la carga no se encuentran en el excel cargado. Se recomienda seguir el formato de la plantilla.'}}
        else:
            if len(request.POST)>1:
                context = {'errors':{[key for key in list(request.POST.keys()) if key != 'csrfmiddlewaretoken'][0]:['No se cargo ningún excel, es obligatorio subir el archivo a cargar.']}}
        return render(request, self.template_name, context) 
    
class downloadFormatos(View):
    def getFormato(self, excel, filename):
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            excel.to_excel(writer, sheet_name=filename.split(' ')[1])
            writer.save()
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
    def get(self, request, *args, **kwargs):
        if kwargs['tipo'] == 'niveles':
            excel = pd.read_excel(os.path.join(BASE_DIR, r'Formatos\Niveles.xlsx'))
            return self.getFormato(excel, 'Formato niveles')
        elif kwargs['tipo'] == 'instructores':
            excel = pd.read_excel(os.path.join(BASE_DIR, r'Formatos\Instructores.xlsx'))
            return self.getFormato(excel, 'Formato instructores')
        elif kwargs['tipo'] == 'alumnos':
            excel = pd.read_excel(os.path.join(BASE_DIR, r'Formatos\Alumnos.xlsx'))
            return self.getFormato(excel, 'Formato alumnos')
        else:
            return redirect('cargasMasivas')