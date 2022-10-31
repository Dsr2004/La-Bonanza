from datetime import date, datetime, time
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from La_Bonanza. mixins import IsAdminMixin
from .models import Picadero, InfoPicadero as infoPicaderoModel
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
                clases = InformacionPicadero.clases.all()
                clasesList=[]
                for clase in clases:
                    clasesList.append({"estudiante":clase.calendario.registro.get_estudiante, "profesor":clase.profesor.get_profesor})
                print(clasesList)
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
