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
            'placeholder':'Confirme la nueva contraseña'
        }
    ))
    passwordA = forms.CharField(label="Contraseña antigua",widget=forms.PasswordInput(
        attrs={
            'id':"newpassword",
            'requerid':'requerid',
            'name':'passwordA',
            "class":"form-control",
            'placeholder':'Ingrese la contraseña actual'
        }
    ))
    
    class Meta:
        model = Usuario
        
        fields=['password']
        widgets={
            'password': forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "off",'id':"password",'requerid':'requerid','name':'password', 'placeholder':'Ingrese la nueva contraseña'}),
        }
    def clean_password2(self):
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
            "usuario": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Ingrese el nombre de usuario"}),
            "nombres": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Ingrese el nombre completo"}),
            "apellidos": forms.DateInput(attrs={"class":"form-control", "autocomplete":"off","placeholder":"Ingrese los apellidos"}),
            "cedula": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off","placeholder":"Ingrese la cédula de la persona"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type":"date", "class":"form-control", "autocomplete":"off"},format=('%Y-%m-%d'),),
            "email": forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Ingrese el correo electrónico"}),
            "celular": forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Ingrese el número de celular"}),
            
        }   