from django import forms
from .models import Estudiante, Registro, Profesor

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("nombre_completo","fecha_nacimiento","documento", "celular","telefono","email",
        "direccion","barrio","ciudad","seguro_medico","documento_identidad",
        "nombre_completo_acudiente","cedula_acudiente","lugar_expedicion_acudiente","celular_acudiente","email_acudiente",
        "nombre_contactoE","telefono_contactoE","relacion_contactoE", "documento_A", "seguro_A", "firma")

        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "fecha_nacimiento":forms.DateInput(attrs={"type":"text","class":"form-control", "autocomplete":"off"}),
            "documento": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "celular": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "telefono": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "email": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "direccion": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "barrio": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "ciudad": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "seguro_medico": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "documento_identidad": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "nombre_completo_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "cedula_acudiente": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "lugar_expedicion_acudiente": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "celular_acudiente": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "email_acudiente": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "documento_A" : forms.FileInput(attrs={"class":"form-control"}),
            "seguro_A" : forms.FileInput(attrs={"class":"form-control"}),
            "firma" : forms.FileInput(attrs={"class":"form-control"})

        }    


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = "__all__"

        widgets = {
            "pagado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "inicioClase": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "finClase": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "horaClase": forms.TimeInput(attrs={"type":"time", "class":"form-control", "autocomplete":"off"}),
            "diaClase": forms.SelectMultiple(attrs={"class":"form-select"}),
            "nivel": forms.Select(attrs={"class":"form-select"}),
            "profesor": forms.Select(attrs={"class":"form-select"}),
        }
        
class ProfesorForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Profesor
        fields = ['niveles','trabaja_sabado']
        widgets = {
            "niveles": forms.SelectMultiple(attrs={"class":"form-select selectpicker", "autocomplete":"off", "multiple":'multiple', 'data-live-search':"true"}),
            "trabaja_sabado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        }