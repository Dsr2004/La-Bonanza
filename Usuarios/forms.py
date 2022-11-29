from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label = "Nombre de Usuario",
        widget = forms.TextInput(attrs={'autofocus': True,"class":"form-control inpr","id":"inputUsuario","placeholder":"Nombre de usuario"})
    )

    password  = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Contraseña", "required":"True"})
        )
    
class CambiarContrasena(forms.ModelForm):
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(
        attrs={
            'id':"confpassword",
            'requerid':'requerid',
            'name':'passwordC',
            "class":"form-control",
        }
    ))
    passwordA = forms.CharField(label="Contraseña antigua",widget=forms.PasswordInput(
        attrs={
            'id':"newpassword",
            'requerid':'requerid',
            'name':'passwordA',
            "class":"form-control",
        }
    ))
    
    class Meta:
        model = Usuario
        
        fields=['password']
        widgets={
            'password': forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "off",'id':"password",'requerid':'requerid','name':'password',}),
        }
    def clean_password2(self):
        """Validación de contraseña
        
        
        Metodo que valida que ambas contraseñas ingresadas sean iguales, antes de ser encriptadas, Retorna la contraseña Validada.
        """
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordC')
        
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UsuarioForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Usuario
        fields = ['usuario','nombres','apellidos','cedula','fecha_nacimiento','email','celular']
        widgets = {
            "usuario": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "nombres": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "apellidos": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "cedula": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type":"date", "class":"form-control", "autocomplete":"off"},format=('%Y-%m-%d'),),
            "email": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}),
            "celular": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}),
            
        }   