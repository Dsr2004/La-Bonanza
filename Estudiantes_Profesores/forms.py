from tkinter import Widget
from django import forms
from .models import Estudiante, Registro

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"
        widgets = {
            "fecha_nacimiento":forms.DateTimeInput(),
        }


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = "__all__"