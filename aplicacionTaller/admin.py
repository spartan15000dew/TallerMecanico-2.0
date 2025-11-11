from django.contrib import admin
from .models import Login, Cliente, Mecanico, Vehiculo, Cita, Servicio, Historial

# Personalización para el modelo Login
@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
    list_filter = ('rol',)
    search_fields = ('user',)
    list_per_page = 25

# Personalización para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono', 'get_login_user')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_per_page = 25
    
    # Para mostrar el usuario del modelo Login relacionado
    @admin.display(description='Usuario (Login)')
    def get_login_user(self, obj):
        return obj.login.user

# Personalización para el modelo Mecanico
@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    # Nota: Tu modelo 'Mecanico' define 'ESPECIALIDAD_CHOICES' 
    # pero no las usa en el campo 'especialidad'.
    # Si quieres un desplegable, tu models.py debería tener:
    # especialidad = models.CharField(max_length=45, choices=ESPECIALIDAD_CHOICES)
    
    list_display = ('nombre', 'especialidad', 'telefono', 'get_login_user')
    list_filter = ('especialidad',)
    search_fields = ('nombre', 'especialidad')
    list_per_page = 25

    # Para mostrar el usuario del modelo Login relacionado
    @admin.display(description='Usuario (Login)')
    def get_login_user(self, obj):
        return obj.login.user

# Personalización para el modelo Vehiculo
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'año', 'cliente')
    list_filter = ('marca', 'año', 'cliente')
    search_fields = ('patente', 'marca', 'modelo', 'cliente__nombre', 'cliente__apellido')
    # raw_id_fields es útil si tienes muchos clientes, para no cargar un desplegable gigante
    raw_id_fields = ('cliente',)
    list_per_page = 25

# Personalización para el modelo Cita
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('vehiculo__patente', 'vehiculo__marca')
    raw_id_fields = ('vehiculo',)
    date_hierarchy = 'fecha' # Añade una navegación por fechas
    list_per_page = 25

# Personalización para el modelo Servicio
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'costo', 'cita', 'mecanico')
    list_filter = ('mecanico', 'nombre_servicio')
    search_fields = ('nombre_servicio', 'cita__vehiculo__patente')
    raw_id_fields = ('cita', 'mecanico')
    list_per_page = 25

# Personalización para el modelo Historial
@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_realizacion', 'mecanico', 'costo_final')
    list_filter = ('fecha_realizacion', 'mecanico')
    search_fields = ('detalle_trabajo', 'mecanico__nombre')
    raw_id_fields = ('mecanico',)
    date_hierarchy = 'fecha_realizacion'
    list_per_page = 25