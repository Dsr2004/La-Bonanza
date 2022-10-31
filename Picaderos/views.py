from ast import Try
from calendar import calendar
from datetime import date, datetime, time
from gc import get_objects
from pipes import Template
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from Estudiantes_Profesores.models import Profesor
from La_Bonanza. mixins import IsAdminMixin
from .models import Clase, EstadoClase, Picadero, InfoPicadero as infoPicaderoModel
from .forms import PicaderoForm
from Estudiantes_Profesores.views.views import arreglarFormatoDia

class Picaderos(IsAdminMixin, ListView):
    model = Picadero
    template_name = "picaderos.html"
    context_object_name = "picaderos"


class InfoPicadero(IsAdminMixin, DetailView):
    model = Picadero
    template_name = "verPicadero.html"
    context_object_name = "picadero"

    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        hora = datetime.now().time()
        hora = time(hora.hour,0,0)
        dia = datetime.now().weekday()
        dia = arreglarFormatoDia(dia)
        try:
            InformacionPicadero = infoPicaderoModel.objects.get(picadero=self.get_object(),hora=hora)
            contexto["clases"]= InformacionPicadero.clases.all()
        except:
            InformacionPicadero = []
        contexto["infoPicadero"]=InformacionPicadero
       
        contexto["hora"]=hora
        contexto["dia"]=dia
       
        return contexto
    
    def post(self, request, *args, **kwargs):
        hora = request.POST.get("hora")
        dia = request.POST.get("dia")
        if hora:
            hora = datetime.strptime(hora, "%H:%M").time()
            hora=time(hora.hour,0,0)
            try:
                InformacionPicadero = infoPicaderoModel.objects.get(picadero=self.get_object(),hora=hora,dia=dia)
                clases = EstadoClase.objects.filter(InfoPicadero = InformacionPicadero)
                clasesList=[]
                for clase in clases:
                    if (clase.dia-datetime.now().date()).days + 1 > 0 and (clase.dia-datetime.now().date()).days + 1 <7:
                        clasesList.append({'id':clase.clase.pk,"estudiante":clase.clase.calendario.registro.get_estudiante, "profesor":clase.clase.profesor.get_profesor})
                return JsonResponse({"clases":clasesList},status=200)
            except Exception as e:
                print("no", str(e))
                return JsonResponse({"error":"No se encontraron Clases en esa Hora"},status=400)
            
        

class CrearPicadero(IsAdminMixin, CreateView):
    model = Picadero
    template_name = "Picaderos/crearPicadero.html"
    form_class = PicaderoForm
    success_url= reverse_lazy("picaderos")
    
    def form_invalid(self, form):
        return JsonResponse({"errores":form.errors}, status=400)

class ModificarPicadero(IsAdminMixin, UpdateView):
    model = Picadero
    template_name = "Picaderos/modificarPicadero.html"
    form_class = PicaderoForm
    success_url= reverse_lazy("picaderos")
    
    def form_invalid(self, form):
        return JsonResponse({"errores":form.errors}, status=400)
    
    
class BorrarPicadero(View):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            id = request.POST.get("id")
            try:
                picadero = Picadero.objects.get(pk=id)
                picadero.delete()
                return JsonResponse({"mensaje":"se borro el picadero satisfactoriamente"}, status=200)
            except:
                print("ha ocurrido error")
                return JsonResponse({"error":"no se pudo encontrar el picadero porque no existe"}, status=400)


class editarProfesorClase(TemplateView):
    model = Clase
    def get(self, request, *args, **kwargs):
        try:
            clase = EstadoClase.objects.get(clase = self.model.objects.get(pk=kwargs['pk']))
        except Exception as e:
            if str(e) == 'Clase matching query does not exist.':
                return JsonResponse({"error":"La consulta que se busca no existe o fue modificada recientemente, por favor intentelo nuevamente","type":True}, status=400)
            else:
                return JsonResponse({"error":"Ocurrio un error interno en el servidor, por favor intentelo mas tarde","type":False}, status=400)
        profesores = [profesor.pk for profesor in Profesor.objects.all() if clase.InfoPicadero.picadero.nivel in profesor.niveles.all()]
        calendario = clase.clase.calendario
        data = {'Profesores':{'profesoresPk':profesores,'profesoresName': [profesor.usuario.nombres for profesor in Profesor.objects.all() if clase.InfoPicadero.picadero.nivel in profesor.niveles.all()]}, 'ActualProfesor':{'ProfesorPk':clase.clase.profesor.pk,'ProfesorName':clase.clase.profesor.usuario.nombres}, 'nombreEstudiante':calendario.registro.estudiante.nombre_completo}
        return JsonResponse(data, status=200)
    def post(self, request, *args, **kwargs):
        try:
            Eclase = EstadoClase.objects.get(clase = self.model.objects.get(pk=kwargs['pk']))
            clase = Eclase.clase
            clase.profesor = Profesor.objects.get(pk =request.POST['profesor'])
            clase.save()
            return redirect('../InfoPicadero/'+str(Eclase.InfoPicadero.picadero.slug))
        except Exception as e:
            return JsonResponse({'error':f'No se pudo realizar la modificación porque {str(e)}'}, status=400)
            