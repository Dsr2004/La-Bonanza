from datetime import datetime, timedelta
import json
from django import forms
from .models import Estudiante, Registro, Profesor
from django.core.exceptions import ValidationError
from Usuarios.models import Usuario
class CrearEstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","nombre_completo","fecha_nacimiento","documento", "celular","email","direccion",
        "barrio","ciudad","seguro","poliza","comprobante_seguro_medico",
        "comprobante_documento_identidad","nombre_completo_madre","cedula_madre","celular_madre",
        "email_madre","nombre_completo_padre","cedula_padre", "celular_padre", "email_padre","nombre_contactoE","telefono_contactoE","relacion_contactoE","exoneracion",
        "documento_A","seguro_A","tipo_clase","aceptaContrato","facturacion_electronica",'tipo_servicio',"nombre_facturar", "identificacion_facturar","direccion_facturar","email_facturar",'nota','autorizaClub')

        widgets = {
        "nombre_completo": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "primer_nombre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "segundo_nombre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "primer_apellido": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "segundo_apellido": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "fecha_nacimiento": forms.DateInput(attrs={"type":"date","class":"form-control", "autocomplete":"off"},format=('%Y-%m-%d')),
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
        "celular_madre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_madre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_completo_padre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "cedula_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "celular_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_padre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_facturar": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "identificacion_facturar": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "direccion_facturar": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "exoneracion": forms.FileInput(attrs={"class":"form-control"}),
        "email_facturar": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "documento_A": forms.FileInput(attrs={"class":"form-control"}),
        "seguro_A": forms.FileInput(attrs={"class":"form-control"}),
        "tipo_clase": forms.Select(attrs={"class":"form-select"}),
        "tipo_servicio": forms.Select(attrs={"class":"form-select"}),
        "nota": forms.Textarea(attrs={"class":"form-control", "autocomplete":"off"}),
        "facturacion_electronica": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        }
    def __init__(self, *args, **kwargs):
        super(CrearEstudianteForm, self).__init__(*args, **kwargs)
        self.fields['primer_nombre'].required = True
        self.fields['segundo_nombre'].required = False
        self.fields['primer_apellido'].required = True
        self.fields['segundo_apellido'].required = True
        self.fields['nombre_completo'].required = False
        self.fields['fecha_nacimiento'].required = True
        self.fields['documento'].required = True
        self.fields['nota'].required = False
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
        self.fields['celular_madre'].required = False
        self.fields['email_madre'].required = False
        self.fields['nombre_completo_padre'].required = False
        self.fields['cedula_padre'].required = False
        self.fields['celular_padre'].required = False
        self.fields['email_padre'].required = False
        self.fields['nombre_contactoE'].required = True
        self.fields['telefono_contactoE'].required = True
        self.fields['relacion_contactoE'].required = True
        self.fields['nombre_facturar'].required = True
        self.fields['identificacion_facturar'].required = True
        self.fields['direccion_facturar'].required = True
        self.fields['email_facturar'].required = True
        self.fields['exoneracion'].required = True
        self.fields['documento_A'].required = True
        self.fields['seguro_A'].required = True
        self.fields['tipo_clase'].required = True
        self.fields['tipo_servicio'].required = True
        self.fields['aceptaContrato'].required = False
        self.fields['facturacion_electronica'].required = False
    def clean_primer_nombre(self):    
        self.nombre = self.cleaned_data['primer_nombre']
        if self.nombre != None:
            if any(map(str.isdigit, self.nombre)):
                raise forms.ValidationError('El nombre no puede contener digitos')
        return self.nombre
    def clean_segundo_nombre(self):    
        self.Lnombre = self.cleaned_data['segundo_nombre']
        if self.Lnombre != None:
            if any(map(str.isdigit, self.Lnombre)):
                raise forms.ValidationError('El nombre no puede contener digitos')
        return self.Lnombre
    def clean_primer_apellido(self):    
        self.apellido = self.cleaned_data['primer_apellido']
        if self.apellido != None:
            if any(map(str.isdigit, self.apellido)):
                raise forms.ValidationError('El apellido no puede contener digitos')
        return self.apellido
    def clean_segundo_apellido(self):    
        self.Lapellido = self.cleaned_data['segundo_apellido']
        if self.Lapellido != None:
            if any(map(str.isdigit, self.Lapellido)):
                raise forms.ValidationError('El apellido no puede contener digitos')
        return self.Lapellido
    def clean_nombre_completo(self):
        try:
            nombre = self.nombre
            if self.Lnombre != None:
                nombre = nombre + f' {self.Lnombre}'
            nombre = nombre + f' {self.apellido} {self.Lapellido}'
            return nombre
        except:
            return None
    def clean_aceptaContrato(self):
        contrato = self.cleaned_data["aceptaContrato"]
        if contrato:
            return contrato
        else:
            raise forms.ValidationError('Si no acepta el reglamento no podrá realizar el registro')
        
    def clean_documento(self):
        documento = self.cleaned_data["documento"]
        if len(str(documento))<=15:
            return documento
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular(self):
        celular = self.cleaned_data["celular"]
        if len(str(celular))<=15:
            return celular
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_cedula_madre(self):
        cedula_madre = self.cleaned_data["cedula_madre"]
        if len(str(cedula_madre))<=15:
            return cedula_madre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular_madre(self):
        celular_madre = self.cleaned_data["celular_madre"]
        if len(str(celular_madre))<=15:
            return celular_madre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
        
    def clean_cedula_padre(self):
        cedula_padre = self.cleaned_data["cedula_padre"]
        if len(str(cedula_padre))<=15:
            return cedula_padre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular_padre(self):
        celular_padre = self.cleaned_data["celular_padre"]
        if len(str(celular_padre))<=15:
            return celular_padre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_telefono_contactoE(self):
        telefono_contactoE = self.cleaned_data["telefono_contactoE"]
        if len(str(telefono_contactoE))<=15:
            return telefono_contactoE
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","nombre_completo","fecha_nacimiento","documento", "celular","email","direccion",
        "barrio","ciudad","seguro","poliza","comprobante_seguro_medico",
        "comprobante_documento_identidad","nombre_completo_madre","cedula_madre","celular_madre",
        "email_madre","nombre_completo_padre","cedula_padre", "celular_padre", "email_padre","nombre_contactoE","telefono_contactoE","relacion_contactoE","exoneracion",
        "documento_A","seguro_A","tipo_clase","aceptaContrato","facturacion_electronica",'tipo_servicio',"nombre_facturar", "identificacion_facturar","direccion_facturar","email_facturar","nota")

        widgets = {
        "nombre_completo": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "primer_nombre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "segundo_nombre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "primer_apellido": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "segundo_apellido": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "fecha_nacimiento": forms.DateInput(attrs={"type":"date","class":"form-control", "autocomplete":"off"},format=('%Y-%m-%d')),
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
        "celular_madre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_madre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_completo_padre": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "cedula_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "celular_padre": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "email_padre": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "telefono_contactoE": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "relacion_contactoE": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nombre_facturar": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "nota": forms.Textarea(attrs={"class":"form-control", "autocomplete":"off"}),
        "identificacion_facturar": forms.NumberInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "direccion_facturar": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "exoneracion": forms.FileInput(attrs={"class":"form-control"}),
        "email_facturar": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
        "documento_A": forms.FileInput(attrs={"class":"form-control"}),
        "seguro_A": forms.FileInput(attrs={"class":"form-control"}),
        "tipo_clase": forms.Select(attrs={"class":"form-select"}),
        "tipo_servicio": forms.Select(attrs={"class":"form-select"}),
        "facturacion_electronica": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
        }
    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['primer_nombre'].required = True
        self.fields['segundo_nombre'].required = False
        self.fields['primer_apellido'].required = True
        self.fields['segundo_apellido'].required = True
        self.fields['nombre_completo'].required = False
        self.fields['fecha_nacimiento'].required = True
        self.fields['documento'].required = True
        self.fields['celular'].required = False
        self.fields['email'].required = False
        self.fields['direccion'].required = True
        self.fields['barrio'].required = True
        self.fields['nota'].required = False
        self.fields['ciudad'].required = True
        self.fields['seguro'].required = False
        self.fields['poliza'].required = False
        self.fields['comprobante_seguro_medico'].required = False
        self.fields['comprobante_documento_identidad'].required = False
        self.fields['nombre_completo_madre'].required = False
        self.fields['cedula_madre'].required = False
        self.fields['celular_madre'].required = False
        self.fields['email_madre'].required = False
        self.fields['nombre_completo_padre'].required = False
        self.fields['cedula_padre'].required = False
        self.fields['celular_padre'].required = False
        self.fields['email_padre'].required = False
        self.fields['nombre_contactoE'].required = True
        self.fields['telefono_contactoE'].required = True
        self.fields['relacion_contactoE'].required = True
        self.fields['nombre_facturar'].required = True
        self.fields['identificacion_facturar'].required = True
        self.fields['direccion_facturar'].required = True
        self.fields['email_facturar'].required = True
        self.fields['exoneracion'].required = True
        self.fields['documento_A'].required = True
        self.fields['seguro_A'].required = True
        self.fields['tipo_clase'].required = True
        self.fields['tipo_servicio'].required = True
        self.fields['aceptaContrato'].required = False
        self.fields['facturacion_electronica'].required = False
    def clean_documento(self):
        documento = self.cleaned_data["documento"]
        if len(str(documento))<=15:
            return documento
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular(self):
        celular = self.cleaned_data["celular"]
        if len(str(celular))<=15:
            return celular
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_cedula_madre(self):
        cedula_madre = self.cleaned_data["cedula_madre"]
        if len(str(cedula_madre))<=15:
            return cedula_madre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular_madre(self):
        celular_madre = self.cleaned_data["celular_madre"]
        if len(str(celular_madre))<=15:
            return celular_madre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
        
    def clean_cedula_padre(self):
        cedula_padre = self.cleaned_data["cedula_padre"]
        if len(str(cedula_padre))<=15:
            return cedula_padre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_celular_padre(self):
        celular_padre = self.cleaned_data["celular_padre"]
        if len(str(celular_padre))<=15:
            return celular_padre
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')
    def clean_telefono_contactoE(self):
        telefono_contactoE = self.cleaned_data["telefono_contactoE"]
        if len(str(telefono_contactoE))<=15:
            return telefono_contactoE
        else:
            raise forms.ValidationError('Asegúrese de que este valor sea menor o igual a 15.')


class RegistroForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (RegistroForm,self ).__init__(*args,**kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(usuario__in = [x for x in Usuario.objects.filter(estado=True)])
    class Meta:
        model = Registro
        fields = "__all__"

        widgets = {
            "pagado": forms.CheckboxInput(attrs={"class":"form-check-input", "autocomplete":"off"}),
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