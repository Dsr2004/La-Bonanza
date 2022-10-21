from datetime import datetime, timedelta
import json
from django import forms
from .models import Estudiante, Registro, Profesor
from django.core.exceptions import ValidationError
from .models import DIAS_SEMANA


class CrearEstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("nombre_completo","fecha_nacimiento","documento", "celular","email","direccion",
        "barrio","ciudad","seguro","poliza","comprobante_seguro_medico",
        "comprobante_documento_identidad","nombre_completo_madre","cedula_madre","lugar_expedicion_madre","celular_madre",
        "email_madre","nombre_completo_padre","cedula_padre","lugar_expedicion_padre", "celular_padre", "email_padre", "direccion_A","barrio_A",
        "ciudad_A","nombre_contactoE","telefono_contactoE","relacion_contactoE","firma",
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
        "direccion_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "barrio_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "ciudad_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "firma": forms.FileInput(attrs={"class":"form-control"}),
        "documento_A": forms.FileInput(attrs={"class":"form-control"}),
        "seguro_A": forms.FileInput(attrs={"class":"form-control"}),
        "tipo_clase": forms.Select(attrs={"class":"form-select"}),
        }
    def __init__(self, *args, **kwargs):
        super(CrearEstudianteForm, self).__init__(*args, **kwargs)
        self.fields['nombre_completo'].required = True
        self.fields['fecha_nacimiento'].required = True
        self.fields['documento'].required = True
        self.fields['celular'].required = False
        self.fields['email'].required = False
        self.fields['direccion'].required = True
        self.fields['barrio'].required = True
        self.fields['ciudad'].required = True
        self.fields['seguro'].required = False
        self.fields['poliza'].required = False
        self.fields['comprobante_seguro_medico'].required = False
        self.fields['comprobante_documento_identidad'].required = False
        self.fields['nombre_completo_madre'].required = False
        self.fields['cedula_madre'].required = False
        self.fields['lugar_expedicion_madre'].required = False
        self.fields['celular_madre'].required = False
        self.fields['email_madre'].required = False
        self.fields['nombre_completo_padre'].required = False
        self.fields['cedula_padre'].required = False
        self.fields['lugar_expedicion_padre'].required = False
        self.fields['celular_padre'].required = False
        self.fields['email_padre'].required = False
        self.fields['direccion_A'].required = False
        self.fields['barrio_A'].required = False
        self.fields['ciudad_A'].required = False
        self.fields['nombre_contactoE'].required = True
        self.fields['telefono_contactoE'].required = True
        self.fields['relacion_contactoE'].required = True
        self.fields['firma'].required = True
        self.fields['documento_A'].required = True
        self.fields['seguro_A'].required = True
        self.fields['tipo_clase'].required = True
        self.fields['aceptaContrato'].required = False


    def clean_aceptaContrato(self):
        contrato = self.cleaned_data["aceptaContrato"]
        if contrato:
            return contrato
        else:
            raise forms.ValidationError('Si no acepta el contrato no podrá realizar el registro')

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("nombre_completo","fecha_nacimiento","documento", "celular","email","direccion",
        "barrio","ciudad","seguro","poliza","comprobante_seguro_medico",
        "comprobante_documento_identidad","nombre_completo_madre","cedula_madre","lugar_expedicion_madre","celular_madre",
        "email_madre","nombre_completo_padre","cedula_padre","lugar_expedicion_padre", "celular_padre", "email_padre", "direccion_A","barrio_A",
        "ciudad_A","nombre_contactoE","telefono_contactoE","relacion_contactoE","firma",
        "documento_A","seguro_A","tipo_clase","estado")

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
        "direccion_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "barrio_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "ciudad_A": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "firma": forms.FileInput(attrs={"class":"form-control"}),
        "documento_A": forms.FileInput(attrs={"class":"form-control"}),
        "seguro_A": forms.FileInput(attrs={"class":"form-control"}),
        "tipo_clase": forms.Select(attrs={"class":"form-select"}),
        }
    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['nombre_completo'].required = True
        self.fields['fecha_nacimiento'].required = True
        self.fields['documento'].required = True
        self.fields['celular'].required = False
        self.fields['email'].required = False
        self.fields['direccion'].required = True
        self.fields['barrio'].required = True
        self.fields['ciudad'].required = True
        self.fields['seguro'].required = False
        self.fields['poliza'].required = False
        self.fields['comprobante_seguro_medico'].required = False
        self.fields['comprobante_documento_identidad'].required = False
        self.fields['nombre_completo_madre'].required = False
        self.fields['cedula_madre'].required = False
        self.fields['lugar_expedicion_madre'].required = False
        self.fields['celular_madre'].required = False
        self.fields['email_madre'].required = False
        self.fields['nombre_completo_padre'].required = False
        self.fields['cedula_padre'].required = False
        self.fields['lugar_expedicion_padre'].required = False
        self.fields['celular_padre'].required = False
        self.fields['email_padre'].required = False
        self.fields['direccion_A'].required = False
        self.fields['barrio_A'].required = False
        self.fields['ciudad_A'].required = False
        self.fields['nombre_contactoE'].required = True
        self.fields['telefono_contactoE'].required = True
        self.fields['relacion_contactoE'].required = True
        self.fields['firma'].required = True
        self.fields['documento_A'].required = True
        self.fields['seguro_A'].required = True
        self.fields['tipo_clase'].required = True


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
    def clean_diaClase(self):
        diaClase = self.cleaned_data["diaClase"]
        self.diaClase = diaClase
        return diaClase
    
    def clean_horaClase(self):
        horaClase = self.cleaned_data["horaClase"]
        self.horaClase = horaClase
        return horaClase
    
    def clean_profesor(self):
        profesor = self.cleaned_data["profesor"]
        horario = profesor.horarios
        horario = json.loads(horario)
        hora = self.horaClase.replace(minute = 0, second = 0).strftime('%I:%M %p')
        dias = [str(i[1]) for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in self.diaClase]]
        diasNo = 'los días '+', '.join([str(i[1]) for i in [dia for dia in DIAS_SEMANA] if int(i[0]) in [int(cl) for cl in self.diaClase]])+f' a las {hora} el profesor no esta disponible'
        if [hor for hor in [horary for horary in horario if horary['day'] in [dia for dia in dias]] if datetime.strptime(hor['from'], '%H:%M').time() <= self.horaClase and (datetime.strptime(hor['through'], '%H:%M')-timedelta(hours=1)).time() >= self.horaClase] == []:
            raise forms.ValidationError(diasNo)
        else:
            return profesor 
    
    
    def clean_inicioClase(self):
        inicioClase=self.cleaned_data['inicioClase']
        self.inicioClase = inicioClase
        return inicioClase

    def clean_finClase(self):
        finClase=self.cleaned_data['finClase']
        if finClase<self.inicioClase:
            raise forms.ValidationError('La fecha de finalizacion de la clase debe ser mayor al de inicio de la clase')
        return finClase
        
    
class ProfesorForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Profesor
        fields = ['niveles','trabaja_sabado']
        widgets = {
            "niveles": forms.SelectMultiple(attrs={"class":"form-select selectpicker", "autocomplete":"off", "multiple":'multiple', 'data-live-search':"true"}),
            "trabaja_sabado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        }