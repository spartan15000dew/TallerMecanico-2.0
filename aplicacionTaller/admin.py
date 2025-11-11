from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Marca, Cliente, Mecanico, Vehiculo, Cita, Servicio, Historial


@admin.action(description='Aprobar mecánicos seleccionados')
def aprobar_mecanicos(modeladmin, request, queryset):
    queryset.update(aprobado=True)
    try:
        grupo_mecanicos = Group.objects.get(name='Mecanicos')
        for mecanico in queryset:
            mecanico.usuario.groups.add(grupo_mecanicos)
    except Group.DoesNotExist:

        pass 
        

@admin.action(description='Desaprobar mecánicos seleccionados')
def desaprobar_mecanicos(modeladmin, request, queryset):
    queryset.update(aprobado=False)

    try:
        grupo_mecanicos = Group.objects.get(name='Mecanicos')
        for mecanico in queryset:
            mecanico.usuario.groups.remove(grupo_mecanicos)
    except Group.DoesNotExist:
        pass


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'telefono', 'direccion')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefono')

    raw_id_fields = ('usuario',)

    @admin.display(description='Usuario')
    def get_username(self, obj):
        return obj.usuario.username

    @admin.display(description='Nombre Completo')
    def get_full_name(self, obj):
        return obj.usuario.get_full_name()

@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'telefono', 'aprobado')
    list_filter = ('aprobado', 'marcas')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefono')
    raw_id_fields = ('usuario',)
    

    filter_horizontal = ('marcas',) 
    

    actions = [aprobar_mecanicos, desaprobar_mecanicos]

    @admin.display(description='Usuario')
    def get_username(self, obj):
        return obj.usuario.username

    @admin.display(description='Nombre Completo')
    def get_full_name(self, obj):
        return obj.usuario.get_full_name()

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'año', 'cliente')
    list_filter = ('marca', 'año', 'cliente__usuario__first_name')
    search_fields = ('patente', 'marca', 'modelo', 'cliente__usuario__username')
    raw_id_fields = ('cliente',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('get_vehiculo_patente', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('vehiculo__patente', 'vehiculo__marca')
    raw_id_fields = ('vehiculo',)
    date_hierarchy = 'fecha_hora'

    @admin.display(description='Vehículo (Patente)')
    def get_vehiculo_patente(self, obj):
        return obj.vehiculo.patente

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'costo', 'cita', 'mecanico')
    list_filter = ('mecanico__usuario__first_name', 'nombre_servicio')
    search_fields = ('nombre_servicio', 'cita__vehiculo__patente')
    raw_id_fields = ('cita', 'mecanico')

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_realizacion', 'mecanico', 'costo_final')
    list_filter = ('fecha_realizacion', 'mecanico__usuario__first_name')
    search_fields = ('detalle_trabajo', 'mecanico__usuario__first_name')
    raw_id_fields = ('mecanico',)
    date_hierarchy = 'fecha_realizacion'