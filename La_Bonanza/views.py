from django.shortcuts import render
from Usuarios.models import Usuario
from Estudiantes_Profesores.models import Profesor
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.http import HttpResponse, JsonResponse

class index(TemplateView):
    def get(self, request, *args, **kwargs):
        Usuarios =  {
            'Usuarios':Usuario.objects.exclude(pk = request.user.pk),
            'filter':{"value":"All","cont":'Todos'}
        }
        return render(request, "index.html", Usuarios)
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        filter = {"value":"","cont":''}
        print(request.POST)
        Usuarios =  {
            'Usuarios':Usuario.objects.exclude(pk = request.user.pk),
            'filter':filter
        }
        return render(request, "index.html", Usuarios)
@csrf_exempt
def pos(request):
    if request.method == 'POST':
        return  HttpResponse(request, content_type="application/json", status=200)