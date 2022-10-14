from pickle import FALSE
from django.shortcuts import render, redirect
from Usuarios.models import Usuario
from Estudiantes_Profesores.models import Profesor
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.http import HttpResponse, JsonResponse

class index(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        Usuarios =  {
            'Usuarios':Usuario.objects.exclude(pk = request.user.pk),
            'filter':{"value":"All","cont":'Todos'}
        }
        return render(request, "index.html", Usuarios)
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        filter = {"value":"","cont":''}
        filter['value']=request.POST.get('value')
        cont = ''
        usuarios = ''
        if filter['value']=='All':
            cont = 'Todos'
            usuarios = Usuario.objects.exclude(pk = request.user.pk)
        if filter['value']=='P':
            cont = 'Profesores'
            usuarios = Usuario.objects.exclude(pk = request.user.pk).filter(administrador = False)
        if filter['value']=='A':
            cont = 'Administradores'
            usuarios = Usuario.objects.exclude(pk = request.user.pk).filter(administrador = True)
        filter['cont']=cont
        Usuarios =  {
            'Usuarios':usuarios,
            'filter':filter
        }
        return render(request, "index.html", Usuarios)
