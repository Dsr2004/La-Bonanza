import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from Estudiantes_Profesores.models import DIAS_SEMANA, Calendario as CalendarioModel, Clase, Registro
from Picaderos.models import EstadoClase, InfoPicadero, Picadero
from Niveles.models import Nivel

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
    
class ValidationClass():
        
    def HorarioProfesor(self, profesor,dia, hora):
        horario = profesor.horarios
        horario = json.loads(horario)
        dias = []
        for d in DIAS_SEMANA:
            if d[0] == str(dia):
                dias.append(str(d[1]))
        diasNo = 'los días '+str(dias[0])+' a las '+hora.strftime('%I:%M %p')+' el profesor no esta disponible'
        if [hor for hor in [horary for horary in horario if horary['day'] in [dia for dia in dias]] if datetime.strptime(hor['from'], '%H:%M').time() <= hora.time() and (datetime.strptime(hor['through'], '%H:%M')-timedelta(hours=1)).time() >= hora.time()] == []:
            return diasNo
        
    def ValidacionPicadero(self, profesor, dia, hora:datetime, clasepk, estado):
       
        try:
            if estado == "CREADO":
                picadero = Picadero.objects.get(pk = clasepk)
               
            elif estado == "BUSCAR":
                clase = EstadoClase.objects.get(pk = clasepk)
                picadero =  clase.InfoPicadero.picadero
        except:
            return JsonResponse({"errores":{"nivel":"No se puede agregar este estudiante porque no hay un picadero con el nivel seleccionado"}}, status=400)
        errores = [{},{}]
        max_estudiantes = picadero.max_estudiantes
        max_profes = picadero.max_profesores
        picaderos = InfoPicadero.objects.all()
        print(picadero)
        print(hora, type(hora))
        picaderos = picaderos.filter(dia = dia).filter(hora=hora).filter(picadero=picadero)
       
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
                claseSelected = [diasC for diasC in EstadoClase.objects.all() if int(dia) == int(diasC.dia.weekday()) and hora.time() == diasC.clase.calendario.horaClase]
                if len(claseSelected)>0:
                    Clases = [pro.clases.all() for pro in InfoPicadero.objects.filter(picadero=clase.InfoPicadero.picadero) if int(pro.dia) == arreglarFormatoDia(dia.weekday()) and pro.hora == hora.time()]
                    try:
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
                    except:
                        pass
        if errores!=[]:    
            if errores[0]!={}:
                return{"tipo":"estudiante","errores":{"estudiante":[f"No puede asignar este {errores[0]['tipo']} porque el picadero: {errores[0]['contenido']['nombre']} los dias {errores[0]['contenido']['dias']} a las {errores[0]['contenido']['hora']} no admite más estudiantes"]}}
                
            elif errores[1]!={}:
                return{"tipo":"profesor","errores":{"profesor":[f"No puede asignar este {errores[1]['tipo']} porque el picadero: {errores[1]['contenido']['nombre']} los dias {errores[1]['contenido']['dias']} a las {errores[1]['contenido']['hora']} no admite más profesores"]}}
            else:
                 return{"tipo":"NO"}

def guardarRegistro(objecto, diasClases, hora, copia, finClase, diaOriginal):
        picadero = Picadero.objects.get(nivel = objecto.nivel)
        rangeDays = []
        if "meseSus" not in copia:
            for i in range(len(diasClases)):
                first_date = datetime.strptime(diaOriginal[i], '%Y-%m-%d')
                last_date = finClase[i]
                week_day = int(diasClases[i])
                dates = [first_date + timedelta(days=d)-timedelta(days=1)  for d in range((last_date - first_date).days + 1) if int((first_date + timedelta(days=d)).weekday()) == int(week_day)] 
                rangeDays.append(dates)
                calendario = CalendarioModel.objects.create(horaClase=hora[i],finClase=finClase[i],inicioClase=diaOriginal[i],diaClase = str(diasClases[i]), registro=objecto)
                calendario.save()
                iPicadero, creado = InfoPicadero.objects.get_or_create(picadero=picadero,hora=hora[i], dia=diasClases[i]) 
                iPicadero.save()
                for fecha in rangeDays[i]:
                    clase =  Clase.objects.create(calendario=calendario, profesor=objecto.profesor)
                    clase.save()
                    iPicadero.clases.add(clase)
                    claseE = EstadoClase.objects.get(clase=clase)
                    claseE.dia = fecha
                    claseE.save()
            return True
        else:
            for diaClaseF in diasClases:
                first_date = datetime.strptime(diaOriginal, '%Y-%m-%d')
                last_date = finClase
                week_day = int(diaClaseF)
                dates = [first_date + timedelta(days=d)-timedelta(days=1)  for d in range((last_date - first_date).days + 1) if int((first_date + timedelta(days=d)).weekday()) == int(week_day)] 
                rangeDays.append(dates)
            for i in range(len(hora)):
                calendario = CalendarioModel.objects.create(horaClase=hora[i],finClase=finClase,inicioClase=diaOriginal,diaClase = str(diasClases[i]), registro=objecto)
                calendario.save()
                iPicadero, creado = InfoPicadero.objects.get_or_create(picadero=picadero,hora=hora[i], dia=diasClases[i]) 
                iPicadero.save()
                for fecha in rangeDays[i]:
                    clase =  Clase.objects.create(calendario=calendario, profesor=objecto.profesor)
                    clase.save()
                    iPicadero.clases.add(clase)
                    claseE = EstadoClase.objects.get(clase=clase)
                    claseE.dia = fecha
                    claseE.save()
            return True
        