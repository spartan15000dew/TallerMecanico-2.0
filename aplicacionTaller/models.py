from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


telefono_validador = RegexValidator(
    regex=r'^\+?\d{7,15}$', 
    message="Ingrese un número de teléfono válido (7-15 dígitos, opcional +)."
)


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre




class Cliente(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    

    telefono = models.CharField(max_length=15, validators=[telefono_validador])
    direccion = models.CharField(max_length=100)
    
    def __str__(self):

        return f"Cliente: {self.usuario.get_full_name()} ({self.usuario.username})"

class Mecanico(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_mecanico')
    
    telefono = models.CharField(max_length=15, validators=[telefono_validador])
    

    marcas = models.ManyToManyField(Marca, related_name='mecanicos', blank=True)
    

    aprobado = models.BooleanField(default=False)

    def __str__(self):

        estado = "Aprobado" if self.aprobado else "Pendiente"
        return f"Mecánico: {self.usuario.get_full_name()} ({estado})"



class Vehiculo(models.Model):
    patente = models.CharField(max_length=45, unique=True)
    marca = models.CharField(max_length=45) 
    modelo = models.CharField(max_length=45)
    año = models.IntegerField()


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"

class Cita(models.Model):
    fecha = models.DateField()
    estado = models.CharField(max_length=45)

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='citas')

    def __str__(self):
        return f"Cita para {self.vehiculo.patente} el {self.fecha}"

class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=255)
    costo = models.IntegerField() 

    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='servicios')
    

    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_servicio

class Historial(models.Model):
    detalle_trabajo = models.TextField()
    costo_final = models.CharField(max_length=45)
    fecha_realizacion = models.DateField()

    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Historial {self.id} - {self.fecha_realizacion}"