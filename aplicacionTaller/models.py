from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

class Mecanico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Motor', 'Motor'),
        ('Frenos', 'Frenos'),
        ('Suspensión', 'Suspensión'),
        ('Eléctrico', 'Eléctrico'),
        ('Transmisión', 'Transmisión'),
        ('Neumáticos', 'Neumáticos'),
        ('Diagnóstico', 'Diagnóstico Electrónico'),
        ('Mantenimiento', 'Mantenimiento General'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_mecanico')
    
    especialidad = models.CharField(max_length=200, choices=ESPECIALIDAD_CHOICES)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.especialidad}"