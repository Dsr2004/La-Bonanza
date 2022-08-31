from tkinter import Widget
from django import forms
from .models import Estudiante, Registro

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"
        widgets = {
            'fecha_nacimiento':forms.DateInput(
                attrs={
                    'type':'date',
                }
            ),
        }


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = "__all__"