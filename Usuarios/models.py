from platform import mac_ver
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.db import models
from  django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self,usuario,nombres,apellidos,celular,email,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            celular = celular, 
            email = self.normalize_email(email), 
            )
        usuario.set_password(password)
        usuario.save()
        return usuario


    def create_superuser(self,usuario,nombres,apellidos,celular,email,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            celular = celular, 
            email = self.normalize_email(email), 
            )
        usuario.set_password(password)
        usuario.administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    usuario = models.CharField("Usuario", unique=True, max_length=15)
    nombres  = models.CharField("Nombre de usuario", blank=False, null=False, max_length=15)
    celular = models.CharField("Celular del usuario", blank=False, null=False, max_length=10)
    apellidos = models.CharField("Apellido de usuario", blank=False, null=False, max_length=25)
    email = models.EmailField('Correo Electrónico', unique=True)
    estado = models.BooleanField("Estado del usuario", default=True)
    administrador = models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD='usuario' 
    REQUIRED_FIELDS=["nombres", "apellidos","celular","email"]

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
