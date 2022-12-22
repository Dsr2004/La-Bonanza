from django import forms
from .models import Picadero

class PicaderoForm(forms.ModelForm):
    class Meta:
        model = Picadero
        fields = ("nombre", "max_estudiantes","max_profesores","nivel")
        widgets={
            "nombre": forms.TextInput(attrs={"class":"form-control", "placeholder":"Ingrese el nombre del picadero"}),
            "max_estudiantes": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Ingrese el número maximo de alumnos"}),
            "max_profesores": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Ingrese el número maximo de instructores"}),
            "nivel": forms.Select(attrs={"class":"form-select"})
        }