from pyexpat import model
from django import forms
from .models import Nivel

class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = "__all__"

        widgets = {
            "nivel":forms.TextInput(attrs={"class":"form-control"}),
            "color_fondo":forms.TextInput(attrs={"class":"form-control", "type":"color"}),
            "color_letra":forms.TextInput(attrs={"class":"form-control", "type":"color"}),
        }