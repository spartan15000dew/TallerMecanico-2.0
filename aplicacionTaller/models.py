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
    
class Historial(models.Model):
    detaller_trabajo = (models.Model)
    costo_final = (models.Model)
    fecha_realizacion = (models.Model)
    Mecanico_id_mecanico = (models.Model)

class Vehiculo(models.Model):
    id_vehiculo = models.IntegerField()
    patente = models.CharField(max_length=50)
    modelo = models.CharField(max_length=30)
    anio = models.IntegerField(max_length=20)