import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import  ListView, TemplateView
from django.http import JsonResponse, HttpResponse
from Usuarios.models import Usuario
from La_Bonanza. mixins import IsAdminMixin
from ..models import  Registro, Profesor
from ..forms import ProfesorForm


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
            horarios = []
            for horario in json.loads(datos['horarios']):
                if horario['day'] not in [horary['day'] for horary in horarios]:
                    horarios.append(horario)
            print(horarios)
            profesor.horarios = json.dumps(horarios)
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
        # context['horaClase'] = datetime.strptime(str(context['registro'].horaClase), '%H:%M:%S').strftime('%I:%M %p')
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

