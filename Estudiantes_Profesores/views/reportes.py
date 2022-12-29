import pandas as pd
from io import BytesIO
from datetime import datetime, time
from django.views.generic import ListView, View
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import  redirect
from La_Bonanza. mixins import IsAdminMixin
from Picaderos.models import Picadero as PicaderoModel, InfoPicadero as infoPicaderoModel, EstadoClase
from ..models import Asistencia, Estudiante, Registro
from Niveles.models import Nivel


class reporteAsistencia(ListView):
    def post(self, request, *args, **kwargs):
        name = ""
        fechas = request.POST.get('fecha').split(' - ')
        todos = request.POST.get('todos')
        fechas=[datetime.strptime(fechas[0], '%m/%d/%Y').date(), datetime.strptime(fechas[1], '%m/%d/%Y').date()]
        Estudiante,Documento,Nivele,Profesor,Dia,Hora,Estado,Tipo_Clase,Picadero=[[],[],[],[],[],[],[],[],[]]
        if todos == None:
            name = "reporte-asistencia-desde:{fecha1}-hasta:{fecha2}".format(fecha1 = fechas[0], fecha2 = fechas[1])
            for asistencia in Asistencia.objects.all().order_by("dia"):
                if request.user.administrador:
                    if asistencia.dia <= fechas[1] and asistencia.dia >= fechas[0]:
                        Estudiante.append(asistencia.registro.estudiante)
                        Documento.append(asistencia.registro.estudiante.documento)
                        Nivele.append(asistencia.registro.nivel.nivel)
                        Profesor.append(asistencia.registro.profesor)
                        Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                        Hora.append(asistencia.hora.strftime('%I:%M %p'))
                        Estado.append(asistencia.get_estado_display())
                        Tipo_Clase.append(asistencia.registro.estudiante.get_tipo_clase_display())
                        if asistencia.picadero:
                            Picadero.append(asistencia.picadero.nombre)
                        else:
                            Picadero.append("El picadero se ha borrado")
                else:
                    if asistencia.registro.profesor == request.user.pk:
                        if asistencia.dia <= fechas[1] and asistencia.dia >= fechas[0]:
                            Estudiante.append(asistencia.registro.estudiante)
                            Documento.append(asistencia.registro.estudiante.documento)
                            Nivele.append(asistencia.registro.nivel.nivel)
                            Profesor.append(asistencia.registro.profesor)
                            Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                            Hora.append(asistencia.hora.strftime('%I:%M %p'))
                            Estado.append(asistencia.get_estado_display())
                            Tipo_Clase.append(asistencia.registro.estudiante.get_tipo_clase_display())
                            if asistencia.picadero:
                                Picadero.append(asistencia.picadero.nombre)
                            else:
                                Picadero.append("El picadero se ha borrado")
                    
        else:
            name="reporte-todas-las-asistencias"
            if request.user.administrador:
                for asistencia in Asistencia.objects.all().order_by("dia"):
                    Estudiante.append(asistencia.registro.estudiante)
                    Documento.append(asistencia.registro.estudiante.documento)
                    Nivele.append(asistencia.registro.nivel.nivel)
                    Profesor.append(asistencia.registro.profesor)
                    Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                    Hora.append(asistencia.hora.strftime('%I:%M %p'))
                    Estado.append(asistencia.get_estado_display())
                    Tipo_Clase.append(asistencia.registro.estudiante.get_tipo_clase_display())
                    if asistencia.picadero:
                        Picadero.append(asistencia.picadero.nombre)
                    else:
                        Picadero.append("El picadero se ha borrado")
            else:
                for asistencia in Asistencia.objects.all().order_by("dia"):
                    if asistencia.registro.profesor == request.user.pk:
                        Estudiante.append(asistencia.registro.estudiante)
                        Documento.append(asistencia.registro.estudiante.documento)
                        Nivele.append(asistencia.registro.nivel.nivel)
                        Profesor.append(asistencia.registro.profesor)
                        Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                        Hora.append(asistencia.hora.strftime('%I:%M %p'))
                        Estado.append(asistencia.get_estado_display())
                        Tipo_Clase.append(asistencia.registro.estudiante.get_tipo_clase_display())
                        if asistencia.picadero:
                            Picadero.append(asistencia.picadero.nombre)
                        else:
                            Picadero.append("El picadero se ha borrado")
        
        excel = pd.DataFrame()
        excel['Estudiante'] = Estudiante
        excel['Documento'] = Documento
        excel['Nivel'] = Nivele
        excel['Profesor'] = Profesor
        excel['Dia'] = Dia
        excel['Hora'] = Hora
        excel['Estado'] = Estado
        excel['Tipo de Clase'] = Tipo_Clase
        excel['Picadero'] = Picadero
        
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            excel.to_excel(writer, sheet_name='Asistencia')
            writer.save()
            filename = name
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
        return JsonResponse({'hola':fechas})

class reporteEstudiantes(IsAdminMixin, ListView):
    def post(self, request, *args, **kwargs):
        datos = request.POST.get('typeExport')
        print(request.POST)
        consulta = []
        name = ""
        if datos == 'All':
            name = "reporte-Estudiantes"
            consulta = Registro.objects.all()
        elif datos == 'inhabilitados':
            name = "reporte-Estudiantes-inhabilitados"
            for registro in Registro.objects.all():
                if registro.estudiante.estado == 0:
                    consulta.append(registro)
        elif datos == 'habilitados':
            name = "reporte-Estudiantes-habilitados"
            for registro in Registro.objects.all():
                if registro.estudiante.estado == 1:
                    consulta.append(registro)
        elif datos.isdigit():
            for registro in Registro.objects.all():
                if registro.nivel == Nivel.objects.get(pk = datos):
                    name = "reporte-Estudiantes-nivel-"+registro.nivel.nivel
                    consulta.append(registro)
        elif datos == "clase_Puntual":
             for registro in Registro.objects.all():
                if registro.estudiante.tipo_clase == "1":
                    name = "reporte-Estudiantes-clases_puntuales"
                    consulta.append(registro)
        elif datos == "clase_Mensualidad":
             for registro in Registro.objects.all():
                if registro.estudiante.tipo_clase == "2":
                    name = "reporte-Estudiantes-clases_mensualidad"
                    consulta.append(registro)
                    
        if consulta == []:
            messages.add_message(request, messages.WARNING, "No se encontraron estudiantes con este filtro {filtro}, por lo que no se puede realizar el reporte.".format(filtro = datos))
            return redirect('estudiantes')
        # Definir columnas del excel
        # def calculateAge(birthDate): 
        #     today = date.today() 
        #     age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
        #     return age 
        Estudiante, Profesor, Nivele, Estado, Pagado, Tipo_Clase, fecha_de_nacimiento,direccion,barrio,ciudad,seguro,documento,email_madre,celular_madre,lugar_expedicion_madre,nombre_completo_madre,email_padre,celular_padre,lugar_expedicion_padre,nombre_completo_padre,relacion_contactoE,telefono_contactoE,nombre_contactoE,edad,docuemntoq,facturacion = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for row in consulta:
            Estudiante.append(row.estudiante)
            Profesor.append(row.profesor)
            Nivele.append(row.nivel)
            Tipo_Clase.append(row.estudiante.get_tipo_clase_display())
            fecha_de_nacimiento.append(row.estudiante.fecha_nacimiento)
            direccion.append(row.estudiante.direccion)
            barrio.append(row.estudiante.barrio)
            ciudad.append(row.estudiante.ciudad)
            if row.estudiante.comprobante_seguro_medico:
                seguro.append('Si tiene')
            else:
                seguro.append('No tiene')
            if row.estudiante.comprobante_documento_identidad:
                docuemntoq.append('Si tiene')
                documento.append(row.estudiante.documento)
            else:
                docuemntoq.append('No tiene')
                documento.append('No aplica')

            email_madre.append(row.estudiante.email_madre)
            celular_madre.append(row.estudiante.celular_madre)
            lugar_expedicion_madre.append(row.estudiante.lugar_expedicion_madre)
            nombre_completo_madre.append(row.estudiante.nombre_completo_madre)
            email_padre.append(row.estudiante.email_padre)
            celular_padre.append(row.estudiante.celular_padre)
            lugar_expedicion_padre.append(row.estudiante.lugar_expedicion_padre)
            nombre_completo_padre.append(row.estudiante.nombre_completo_padre)
            relacion_contactoE.append(row.estudiante.relacion_contactoE)
            telefono_contactoE.append(row.estudiante.telefono_contactoE)
            nombre_contactoE.append(row.estudiante.nombre_contactoE)
            edad.append(row.estudiante.get_edad)
            if row.estudiante.estado:
                Estado.append("Activo")
            else:
                Estado.append("Inhabilitado")
            if row.pagado:
                Pagado.append("Pagada")
            else:
                Pagado.append("No ha pagado")
            if row.estudiante.facturacion_electronica:
                facturacion.append("SI")
            else:
                facturacion.append("NO") 
            
        excel = pd.DataFrame()
        excel['Estudiante'] = Estudiante
        excel['Profesor'] = Profesor
        excel['Nivel'] = Nivele
        excel['Estado'] = Estado
        excel['Matricula'] = Pagado
        excel['Tipo de Clase'] = Tipo_Clase 
        excel['Fecha de nacimiento'] = fecha_de_nacimiento
        excel['Edad']=edad
        excel['Direccion'] = direccion
        excel['Barrio'] = barrio
        excel['Ciudad'] = ciudad
        excel['Seguro'] = seguro
        excel['Tiene documento de identidad'] = docuemntoq
        excel['Documento de identidad'] = documento
        excel['Email del madre'] = email_madre
        excel['Celular del madre'] = celular_madre
        excel['Lugar de expedición del madre'] = lugar_expedicion_madre
        excel['Nombre del madre'] = nombre_completo_madre
        excel['Relacion con el contacto de emergencia'] = relacion_contactoE
        excel['Teléfono del contacto de emergencia'] = telefono_contactoE
        excel['Nombre del contacto de emergencia'] = nombre_contactoE
        excel['Factiración electrónica'] = facturacion
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            excel.to_excel(writer, sheet_name='Estudiantes')
            writer.save()
            filename = name
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
        return JsonResponse({'hola':'hola'})

class ReportePicadero(IsAdminMixin, View):
    def post(self, request, *args, **kwargs):
        picadero = PicaderoModel.objects.get(pk=self.kwargs["pk"])
        hora = request.POST.get("hora")
        dia = request.POST.get("dia")
        TodoElDia = request.POST.get("TodoElDia")
        if hora:
            hora = datetime.strptime(hora, "%H:%M").time()
            hora=time(hora.hour,0,0)
            try:
                if TodoElDia == "SI":
                    InformacionPicadero = infoPicaderoModel.objects.filter(picadero=picadero).filter(dia=dia)
                    Estudiante, Profesor, Picadero, Dia, Hora =[[],[],[],[],[]]
                    for info in InformacionPicadero:
                        clases = info.clases.all()
                        for clase in clases:
                            Estudiante.append(clase.calendario.registro.get_estudiante)
                            Profesor.append(clase.profesor.get_profesor)
                            Picadero.append(picadero.nombre)
                            Dia.append(info.get_dia_display())
                            Hora.append(info.hora.strftime("%I:%M %p")) 
                 
                elif TodoElDia == "NO":
                    InformacionPicadero = infoPicaderoModel.objects.get(picadero=picadero,hora=hora,dia=dia)
                    clases = InformacionPicadero.clases.all()
                    Estudiante, Profesor, Picadero, Dia, Hora =[[],[],[],[],[]]
                    for clase in clases:
                        Estudiante.append(clase.calendario.registro.get_estudiante)
                        Profesor.append(clase.profesor.get_profesor)
                        Picadero.append(picadero.nombre)
                        Dia.append(InformacionPicadero.get_dia_display())
                        Hora.append(hora.strftime("%I:%M %p"))
                
            except Exception as e:
                print(e)
                return JsonResponse({"error":"No se encontraron Clases en esa Hora"},status=400)
        if len(Estudiante) == 0:
            return JsonResponse({"error":"No se encontraron Clases"},status=400)
        excel = pd.DataFrame()
        excel['Estudiante'] = Estudiante
        excel['Profesor'] = Profesor 
        excel['Dia'] = Dia 
        excel['Hora'] = Hora 
        excel['Picadero'] = Picadero
        excel['Caballo'] = ""
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            excel.to_excel(writer, sheet_name='Estudiantes')
            writer.save()
            filename = "ReportePicadero"
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
         
        
class ReporteCalendario(ListView):
    def post(self, request, *args, **kwargs):
        name = ""
        fechas = request.POST.get('fecha').split(' - ')
        fechas=[datetime.strptime(fechas[0], '%m/%d/%Y').date(), datetime.strptime(fechas[1], '%m/%d/%Y').date()]
        Estudiante,Documento,Nivele,Profesor,Dia,Hora,Tipo_Clase,Tipo_Servicio=[[],[],[],[],[],[],[],[]]
        name = "reporte-clases-desde:{fecha1}-hasta:{fecha2}".format(fecha1 = fechas[0], fecha2 = fechas[1])
        for asistencia in EstadoClase.objects.all().order_by("dia"):
            if request.user.administrador:
                if asistencia.dia <= fechas[1] and asistencia.dia >= fechas[0]:
                    Estudiante.append(asistencia.clase.calendario.registro.estudiante)
                    Documento.append(asistencia.clase.calendario.registro.estudiante.documento)
                    Nivele.append(asistencia.clase.calendario.registro.nivel.nivel)
                    Profesor.append(asistencia.clase.profesor)
                    Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                    Hora.append(asistencia.clase.calendario.horaClase.strftime('%I:%M %p'))
                    Tipo_Clase.append(asistencia.clase.calendario.registro.estudiante.get_tipo_clase_display())
                    Tipo_Servicio.append(asistencia.clase.calendario.registro.estudiante.tipo_servicio.nombre)
            else:
                if asistencia.clase.profesor == request.user.pk:
                    if asistencia.dia <= fechas[1] and asistencia.dia >= fechas[0]:
                        Estudiante.append(asistencia.clase.calendario.registro.estudiante)
                        Documento.append(asistencia.clase.calendario.registro.estudiante.documento)
                        Nivele.append(asistencia.clase.calendario.registro.nivel.nivel)
                        Profesor.append(asistencia.clase.profesor)
                        Dia.append(datetime.strftime(asistencia.dia, '%Y/%m/%d'))
                        Hora.append(asistencia.clase.calendario.horaClase.strftime('%I:%M %p'))
                        Tipo_Clase.append(asistencia.clase.calendario.registro.estudiante.get_tipo_clase_display())
                        Tipo_Servicio.append(asistencia.clase.calendario.registro.estudiante.tipo_servicio.nombre)
                       
                       
        excel = pd.DataFrame()
        excel['Estudiante'] = Estudiante
        excel['Documento'] = Documento
        excel['Nivel'] = Nivele
        excel['Profesor'] = Profesor
        excel['Dia'] = Dia
        excel['Hora'] = Hora
        excel['Tipo de Clase'] = Tipo_Clase
        excel['Tipo de Servicio'] = Tipo_Servicio
        
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            excel.to_excel(writer, sheet_name='Asistencia')
            writer.save()
            filename = name
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
