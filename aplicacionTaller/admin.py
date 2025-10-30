from django.contrib import admin
from .models import Cliente, Mecanico

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'get_last_name', 'get_email', 'telefono')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email', 'telefono')

    @admin.display(description='Usuario')
    def get_username(self, obj):
        return obj.usuario.username

    @admin.display(description='Nombre')
    def get_first_name(self, obj):
        return obj.usuario.first_name

    @admin.display(description='Apellido')
    def get_last_name(self, obj):
        return obj.usuario.last_name
    
    @admin.display(description='Correo')
    def get_email(self, obj):
        return obj.usuario.email

@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'especialidad', 'telefono')
    search_fields = ('usuario__username', 'usuario__first_name', 'especialidad', 'telefono')

    @admin.display(description='Usuario')
    def get_username(self, obj):
        return obj.usuario.username

    @admin.display(description='Nombre')
    def get_first_name(self, obj):
        return obj.usuario.first_name