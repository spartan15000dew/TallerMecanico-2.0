from django.db import models
from django.contrib.auth.models import User


class Login(models.Model):

    user = models.CharField(max_length=25, unique=True)
    contrasenia = models.CharField(max_length=100)
    rol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} ({self.rol})"



class Cliente(models.Model):

    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.IntegerField()
    email = models.EmailField(max_length=60) 
    direccion = models.CharField(max_length=45)
    
    login = models.OneToOneField(Login, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Mecanico(models.Model):

    nombre = models.CharField(max_length=45)
    especialidad = models.CharField(max_length=45)
    telefono = models.IntegerField()
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

    login = models.OneToOneField(Login, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"


class Vehiculo(models.Model):
    patente = models.CharField(max_length=45, unique=True)
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    año = models.IntegerField()

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"

class Cita(models.Model):
    fecha = models.DateField()
    estado = models.CharField(max_length=45)

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cita para {self.vehiculo.patente} el {self.fecha}"

class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    costo = models.IntegerField() 

    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_servicio

class Historial(models.Model):

    detalle_trabajo = models.CharField(max_length=80)
    costo_final = models.CharField(max_length=45)
    fecha_realizacion = models.DateField()

    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Historial {self.id} - {self.fecha_realizacion}"