from tkinter import Widget
from django import forms
from .models import Estudiante, Registro, Profesor

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ["nombre_completo","fecha_nacimiento","documento", "celular","telefono","email",
        "direccion","barrio","ciudad","seguro_medico","documento_identidad",
        "nombre_completo_acudiente","cedula_acudiente","lugar_expedicion_acudiente","celular_acudiente","email_acudiente",
        "nombre_contactoE","telefono_contactoE","relacion_contactoE","nivel"]

        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "fecha_nacimiento":forms.DateInput(attrs={'type':'date', "class":"form-control", "autocomplete":"off"}),
            "documento": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "celular": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "telefono": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "email": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "direccion": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "barrio": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "ciudad": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "seguro_medico": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "documento_identidad": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "nombre_completo_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "cedula_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "lugar_expedicion_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "celular_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "email_acudiente": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "telefono_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "nivel": forms.Select(attrs={"class":"form-select"}),
        }


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = "__all__"

        widgets = {
            "pagado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "inicioClase": forms.DateInput(attrs={"type":"date", "class":"form-control", "autocomplete":"off"}),
            "finClase": forms.DateInput(attrs={"type":"date", "class":"form-control", "autocomplete":"off"}),
            "horaClase": forms.TimeInput(attrs={"type":"time", "class":"form-control", "autocomplete":"off"}),
            "diaClase": forms.SelectMultiple(attrs={"class":"form-select"}),
        }
        
class ProfesorForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Profesor
        fields = ['horarios','niveles','trabaja_sabado']
        widgets = {
            "horarios": forms.TextInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "niveles": forms.SelectMultiple(attrs={"class":"form-control", "autocomplete":"off"}),
            "trabaja_sabado": forms.CheckboxInput(attrs={"class":"form-control", "autocomplete":"off"}),
        }