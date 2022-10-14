from django import forms
from .models import Picadero

class PicaderoForm(forms.ModelForm):
    class Meta:
        model = Picadero
        fields = ("nombre", "max_estudiantes","max_profesores","nivel")
        widgets={
            "nombre": forms.TextInput(attrs={"class":"form-control"}),
            "max_estudiantes": forms.NumberInput(attrs={"class":"form-control"}),
            "max_profesores": forms.NumberInput(attrs={"class":"form-control"}),
            "nivel": forms.Select(attrs={"class":"form-select"})
        }