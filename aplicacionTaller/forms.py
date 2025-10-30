from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Cliente, Mecanico

telefono_validador = RegexValidator(regex=r'^\+?\d{7,15}$', message="Ingrese un número de teléfono válido (7-15 dígitos, opcional +).")

class FormularioUsuario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',      
            'last_name': 'Apellido',    
            'email': 'Correo electrónico' 
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data


class FormularioCliente(forms.ModelForm):
    telefono = forms.CharField(validators=[telefono_validador])

    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion'] 
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección'
        }


class FormularioMecanico(forms.ModelForm):
    telefono = forms.CharField(validators=[telefono_validador])
    especialidad = forms.ChoiceField(choices=Mecanico.ESPECIALIDAD_CHOICES, label="Especialidad")

    class Meta:
        model = Mecanico
        fields = ['especialidad', 'telefono']
        labels = {
            'especialidad': 'Especialidad',
            'telefono': 'Teléfono'
        }