from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, CambiarContrasena, UsuarioForm
from Estudiantes_Profesores.forms import ProfesorForm
from .models import Usuario
import json
from django.http import HttpResponse, JsonResponse

class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, *args, **kwargs):
        context={}
        form = LoginForm(request,data=request.POST) #con esto se le pasan los datos al formulario, inserción
        context["form"]=form
        print(request.session)
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            contrasena = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre, password = contrasena)
            print(form.cleaned_data)
            if usuario is not None:
                if usuario.estado == 1:
                    login(request, usuario)
                    if 'next' in request.GET:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect("index")
                else: 
                    context['error']="Este usuario se encuentra inhabilitado"

        else:
            try:
                Usuario.objects.get(usuario=form.cleaned_data.get('username'))
                context['error']="La contraseña es incorrecta"
            except:
                context['error']="El usuario ingresado no existe"
        return render(request, self.template_name, context)

def logout(request):
    logout(request)

class CambiarContrasena(TemplateView):
    model = Usuario
    form_class = CambiarContrasena
    template_name="Usuarios/CambiarContrasena.html" 
    
    def get(self, request, *args, **kwargs):
        contexto={"form":self.form_class}
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        password = request.POST.get('contraseña')
        password2 = request.POST.get('contraseñaC')
        passwordA = request.POST.get('contraseñaA')
        if password == password2:
            if password != passwordA:
                username= request.user.usuario
                user = authenticate(username=username, password=passwordA)
                if user is not None:
                    user.set_password(password)
                    user.save()
                    return JsonResponse({"success":"Succes"})
                else:
                    data = json.dumps({'error': 'La contraseña antigua no es correcta'})
                    return HttpResponse(data, content_type="application/json", status=400)
            else:
                data = json.dumps({'error': 'La nueva contraseña no puede ser igual a la antigua'})
                return HttpResponse(data, content_type="application/json", status=400)
        else:
            data = json.dumps({'error': 'Las contraseñas no coinciden'})
            return HttpResponse(data, content_type="application/json", status=400)
        
class RegistroUsuario(TemplateView):
    def get(self, request, *args, **kwargs):
        tipo = request.GET.get('type')
        data={'formUsuario':UsuarioForm, 'formProfesor':ProfesorForm,'title':'profesor'}
        filter = {"value":"","cont":''}
        filter['value']=request.GET.get('type')
        cont = ''
        if filter['value']=='P' or filter['value']=='All':
            cont = 'Profesores'
        if filter['value']=='A':
            cont = 'Administradores'
        filter['cont']=cont
        data['filter']=filter
        return render(request, 'Usuarios/crearUsuario.html', {'forms':data})
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('function') == 'filtrar':
            tipo = request.POST.get('type')
            filter = {"value":"","cont":''}
            cont = ''
            filter['value']=tipo
            if tipo == 'All' or tipo=='P':
                print(tipo)
                cont = 'Profesores'
                data={'title':'profesor'}
            else:
                data={'title':'administrador'}
                cont = 'Administradores'
            filter['cont']=cont
            data['filter']=filter
            print(data)
            return JsonResponse({"datos":data})
        # return JsonResponse({"success":"Succes"})
        # data = json.dumps({'error': 'Las contraseñas no coinciden'})
        # return HttpResponse(data, content_type="application/json", status=400)
         



