from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Mecanico, Marca, telefono_validador

class FormularioUsuario(forms.ModelForm):
    # El formulario de usuario base para el registro
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre(s)',      
            'last_name': 'Apellido(s)',    
            'email': 'Correo electrónico' 
        }
        help_texts = {
            'username': 'Nombre de usuario único para iniciar sesión.',
        }

    def clean_email(self):
        # Validación para asegurar que el email sea único
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

    def clean(self):
        # Validación para confirmar la contraseña
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data


class FormularioCliente(forms.ModelForm):
    # Formulario para los campos *adicionales* del Cliente
    telefono = forms.CharField(validators=[telefono_validador], label="Teléfono")

    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion'] 
        labels = {
            'direccion': 'Dirección'
        }


class FormularioMecanico(forms.ModelForm):
    # Formulario para los campos *adicionales* del Mecánico
    telefono = forms.CharField(validators=[telefono_validador], label="Teléfono")

    marcas = forms.ModelMultipleChoiceField(
        queryset=Marca.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Marcas en las que se especializa",
        required=True
    )

    class Meta:
        model = Mecanico
        fields = ['telefono', 'marcas']
