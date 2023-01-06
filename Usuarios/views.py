from django.shortcuts import render, redirect
from django.views.generic import View,ListView, CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, CambiarContrasena, UsuarioForm
from Estudiantes_Profesores.forms import ProfesorForm
from Estudiantes_Profesores.models import Profesor
from .models import Usuario
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

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
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            contrasena = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre, password = contrasena)
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
    template_name="Usuarios/cambiarContrasena.html" 
    
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
        if request.user.administrador!=1:
            return redirect("calendario")
        tipo = request.GET.get('type')
        data={'formUsuario':UsuarioForm, 'formProfesor':ProfesorForm,'title':'profesor'}
        filter = {"value":"","cont":''}
        filter['value']=request.GET.get('type')
        cont = ''
        if filter['value']=='P' or filter['value']=='All':
            cont = 'Profesores'
        if filter['value']=='A':
            cont = 'Administradores'
            data['title']='administrador'
        filter['cont']=cont
        data['filter']=filter
        return render(request, 'Usuarios/crearUsuario.html', {'forms':data})
    
    def post(self, request, *args, **kwargs):
        if request.user.administrador!=True:
            return redirect("calendario")
        if request.POST.get('function') == 'filtrar':
            tipo = request.POST.get('type')
            filter = {"value":"","cont":''}
            cont = ''
            filter['value']=tipo
            if tipo == 'All' or tipo=='P':
                cont = 'Profesores'
                data={'title':'profesor'}
            else:
                data={'title':'administrador'}
                cont = 'Administradores'
            filter['cont']=cont
            data['filter']=filter
            return JsonResponse({"datos":data})
        if request.POST.get('function') == 'User' or request.POST.get('function') == 'Teacher':
            usuario=json.loads(request.POST.get('datos'))
            form = UsuarioForm(usuario or None)
            if form.is_valid():
                nombres = form.cleaned_data['nombres'].split(' ')
                nombres = [nombre[0:1] for nombre in nombres]
                apellidos = form.cleaned_data['apellidos'].split(' ')
                apellidos = [nombre[0:1] for nombre in apellidos]
                id = "".join(nombres).upper()+"".join(apellidos).upper()
                try:
                    usuario = Usuario.objects.create(id=id,usuario=form.cleaned_data['usuario'], nombres=form.cleaned_data['nombres'], celular=form.cleaned_data['celular'], apellidos = form.cleaned_data['apellidos'], cedula=form.cleaned_data['cedula'],fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],email = form.cleaned_data['email'])
                except:
                    try:
                        userR = Usuario.objects.get(id = id)
                        if userR.cedula[0:4] != form.cleaned_data['cedula'][0:4]:
                            id = id + form.cleaned_data['cedula'][0:4]
                            usuario = Usuario.objects.create(id=id,usuario=form.cleaned_data['usuario'], nombres=form.cleaned_data['nombres'], celular=form.cleaned_data['celular'], apellidos = form.cleaned_data['apellidos'], cedula=form.cleaned_data['cedula'],fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],email = form.cleaned_data['email'])
                        else:
                            id = id + form.cleaned_data['cedula']
                            usuario = Usuario.objects.create(id=id,usuario=form.cleaned_data['usuario'], nombres=form.cleaned_data['nombres'], celular=form.cleaned_data['celular'], apellidos = form.cleaned_data['apellidos'], cedula=form.cleaned_data['cedula'],fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],email = form.cleaned_data['email'])
                    except:
                        data = json.dumps({'error': 'El usuario que intenta registrar ya existe', 'usuario':form.cleaned_data['usuario']})
                        return HttpResponse(data, content_type="application/json", status=400)
                        
                usuario.set_password(form.cleaned_data['cedula'])
                if request.POST.get('function') == 'User':
                    usuario.administrador = 1
                else:
                    usuario.administrador = 0
                usuario.save()
                return JsonResponse({"datos":id})
            else:
                data = json.dumps({'error': 'Datos ingresados incorrectos', 'forms':form.errors})
                return HttpResponse(data, content_type="application/json", status=400)
        return JsonResponse({"datos":'hola'})
         
class UserFunction(TemplateView):
    template_name = "Usuarios/editarUsuarios.html"
    model = Usuario
    form_class = UsuarioForm
    def get(self,request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        form = {}
        try:
            get_object = Usuario.objects.get(pk=kwargs['pk'])
            if kwargs['pk']==request.user.pk: 
                return redirect('index')
            form = self.form_class(instance=get_object)
        except Exception as e:
            return redirect('login')
        return render(request, self.template_name, {'form':form,'title':get_object.usuario,'pk':get_object.pk})
    
    def post(self, request, *args, **kwargs):
        try:
            get_object = Usuario.objects.get(pk=kwargs['pk'])
            if kwargs['pk']==request.user.pk:  
                return redirect('index')
        except:
            return redirect('index')
        form = self.form_class(request.POST or None, instance=get_object)
        if form.is_valid():
            form.save()
            return JsonResponse({"success":"Succes"})
        else:
            data = json.dumps({'error': 'Datos ingresados incorrectos', 'forms':form.errors})
            return HttpResponse(data, content_type="application/json", status=400)

def EstadoUsuario(request):
    if request.method=="POST":
        id = request.POST["estado"]
        update=Usuario.objects.get(pk=id)
        estado=update.estado
        if estado==True:
            update.estado=False
            update.save()
        elif estado==False:
            update.estado=True
            update.save()
        else:
            return redirect("Inicio")
        return HttpResponse(update)
    else:
        return JsonResponse({"method not allowed":"el metodo no está permitido"})

class Perfil(View):
    def get(self, request, *args, **kwargs):
        form = UsuarioForm(instance=request.user)
        context = {'form': form}
        return render(request, 'Usuarios/Perfil.html', context)

    def post(self, request, *args, **kwargs):
        correo = request.POST.get("email")
        imagen = request.FILES.get("imagen")
        usuario = Usuario.objects.get(pk=request.user.pk)
        if imagen != None:
            usuario.imagen = imagen
            usuario.save()
            messages.success(request, "Se modificó la imagen de perfil.")
        if correo == request.user.email:
            messages.info(request, "No se pudo actualizar el perfil porque el correo es el mismo.")
            return redirect("perfil")
        else:
            usuario.email = correo
            usuario.save()
            messages.success(request, "Se modificó el correo correctamente.")
            return redirect("perfil")

class RestablecerClave(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'Usuarios/RestablecerContrasena.html')
