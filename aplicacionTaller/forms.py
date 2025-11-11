from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Mecanico, Marca, Vehiculo, Cita, telefono_validador

class FormularioUsuario(forms.ModelForm):
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
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data


class FormularioCliente(forms.ModelForm):
    telefono = forms.CharField(validators=[telefono_validador], label="Teléfono")

    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion'] 
        labels = {
            'direccion': 'Dirección'
        }


class FormularioMecanico(forms.ModelForm):
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




class VehiculoForm(forms.ModelForm):
    """Formulario para que el cliente añada/edite sus vehículos."""
    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'año']
        labels = {
            'patente': 'Patente (Placa)',
            'marca': 'Marca (Ej: Volvo, Scania)',
            'modelo': 'Modelo (Ej: FH16, R500)',
            'año': 'Año del modelo',
        }
        widgets = {
            'año': forms.NumberInput(attrs={'min': 1980, 'max': 2025}),
        }

class CitaForm(forms.ModelForm):
    """Formulario para que el cliente solicite una cita."""
    

    fecha_hora = forms.DateTimeField(
        label="Fecha y Hora Solicitada",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    
    class Meta:
        model = Cita
        fields = ['vehiculo', 'fecha_hora', 'motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describa el problema o el servicio que necesita...'}),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        super(CitaForm, self).__init__(*args, **kwargs)
        
        if user and hasattr(user, 'perfil_cliente'):
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(cliente=user.perfil_cliente)
            self.fields['vehiculo'].label = "Seleccione su Vehículo"
        else:
            self.fields['vehiculo'].queryset = Vehiculo.objects.none()