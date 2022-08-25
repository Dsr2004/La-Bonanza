from django.shortcuts import render

def index(request):
    x = request.user
    contexto={"clave":x}
    return render(request, "index.html", contexto)
