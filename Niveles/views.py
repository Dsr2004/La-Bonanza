from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView
from .models import Nivel
from .forms import NivelForm
from django.http import JsonResponse

class Niveles(ListView):
    model=Nivel
    context_object_name="niveles"
    template_name="niveles.html"

class CrearNivel(CreateView):
    model=Nivel
    form_class= NivelForm
    template_name="agregarNivel.html"
    success_url= reverse_lazy("listarNivel")

    def form_invalid(self, form):
        return JsonResponse({"errores":form.errors}, status=400)

class ModificarNivel(UpdateView):
    model=Nivel
    form_class= NivelForm
    template_name="modificarNivel.html"
    success_url= reverse_lazy("listarNivel")

    def form_invalid(self, form):
        return JsonResponse({"errores":form.errors}, status=400)


class BorrarNivel(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get("id")
        try:
            nivel = Nivel.objects.get(pk=id)
            nivel.delete()
            return JsonResponse({"mensaje":"Se ha borrado el nivel de forma satisfactoria"}, status=200)
        except:
            print("error")
            return JsonResponse({"error":"No se encontro el ID "}, status=400) 
        
        