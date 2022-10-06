from django import forms
from .models import Estudiante, Registro, Profesor

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("nombre_completo","fecha_nacimiento","documento", "celular","email","direccion",
        "barrio","ciudad","seguro","poliza","comprobante_seguro_medico",
        "comprobante_documento_identidad","nombre_completo_madre","cedula_madre","lugar_expedicion_madre","celular_madre",
        "email_madre","nombre_completo_padre","cedula_padre","lugar_expedicion_padre", "celular_padre", "email_padre", "direccion","barrio",
        "ciudad","nombre_contactoE","telefono_contactoE","relacion_contactoE","firma",
        "documento_A","seguro_A","tipo_clase","estado","aceptaContrato")

        widgets = {
        "nombre_completo": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "fecha_nacimiento": forms.DateInput(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
        "documento": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "celular": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "direccion": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "barrio": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "ciudad": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "seguro": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "poliza": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "comprobante_seguro_medico": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        "aceptaContrato": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        "comprobante_documento_identidad": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        "nombre_completo_madre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "cedula_madre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "lugar_expedicion_madre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "celular_madre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_madre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_completo_padre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "cedula_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "lugar_expedicion_padre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "celular_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_padre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "direccion": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "barrio": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "ciudad": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "firma": forms.FileInput(attrs={"class":"form-control"}),
        "documento_A": forms.FileInput(attrs={"class":"form-control"}),
        "seguro_A": forms.FileInput(attrs={"class":"form-control"}),
        "tipo_clase": forms.Select(attrs={"class":"form-select"}),
        }    
    def clean_aceptaContrato(self):
        contrato = self.cleaned_data["aceptaContrato"]
        if contrato:
            return contrato
        else:
            raise forms.ValidationError('Si no se acepta el contrato no podrá realizar el registro')

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = "__all__"

        widgets = {
            "pagado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
            "inicioClase": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off", "type":"date"}),
            "finClase": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off", "type":"date"}),
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