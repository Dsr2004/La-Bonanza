from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('CambiarContrasena/', login_required(CambiarContrasena.as_view()), name='changePass'),
]