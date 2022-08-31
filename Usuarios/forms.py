from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label = "Nombre de Usuario",
        widget = forms.TextInput(attrs={'autofocus': True,"class":"form-control","placeholder":"Nombre de usuario"})
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