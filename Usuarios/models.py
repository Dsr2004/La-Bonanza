from enum import unique
from platform import mac_ver
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.db import models
from  django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self,usuario,nombres,apellidos,celular,email,cedula,fecha_nacimiento,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            celular = celular, 
            email = self.normalize_email(email),
            cedula = cedula,
            fecha_nacimiento = fecha_nacimiento 
            )
        usuario.set_password(password)
        usuario.save()
        return usuario


    def create_superuser(self,usuario,nombres,apellidos,celular,email,cedula,fecha_nacimiento,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            celular = celular, 
            email = self.normalize_email(email),
            cedula = cedula,
            fecha_nacimiento = fecha_nacimiento

            )
        usuario.set_password(password)
        usuario.administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=False, null=False)
    usuario = models.CharField("Nombre de Usuario", unique=True, max_length=50)
    nombres  = models.CharField("Nombre completo", blank=False, null=False, max_length=50)
    celular = models.CharField("Celular", blank=False, null=False, max_length=10, unique=True)
    apellidos = models.CharField("Apellidos", blank=False, null=False, max_length=25)
    cedula = models.CharField("Cedula", blank=False, null=False, max_length=25, unique=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento",auto_now=False, auto_now_add=False)
    email = models.EmailField('Correo Electrónico', unique=True)
    estado = models.BooleanField("Estado del usuario", default=True)
    administrador = models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD='usuario' 
    REQUIRED_FIELDS=["nombres", "apellidos","celular","email","cedula","fecha_nacimiento"]

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return '{}'.format(self.nombres+' '+self.apellidos)

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.administrador

