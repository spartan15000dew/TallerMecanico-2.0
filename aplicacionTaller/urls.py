from django.urls import path
from . import views

app_name = "aplicacionTaller"

urlpatterns = [
    # --- Autenticación y Menú ---
    path('', views.rendermMenu, name='menu'), # Página principal
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.renderLogin, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Paneles de Rol ---
    path('servicios/', views.servicios_base, name='servicios_base'),
    path('servicios/cliente/', views.panel_cliente, name='panel_cliente'),
    path('servicios/mecanico/', views.panel_mecanico, name='panel_mecanico'),
    path('servicios/administrador/', views.panel_administrador, name='panel_administrador'),

    # --- Funcionalidad Cliente ---
    path('vehiculos/', views.gestionar_vehiculos, name='gestionar_vehiculos'),
    path('agendar/', views.agendar_cita, name='agendar_cita'),

    # --- Funcionalidad Mecánico ---
    path('citas/detalle/<int:pk>/', views.detalle_cita_mecanico, name='detalle_cita'),

    # --- Vista General de Citas (Reemplaza la estática) ---
    path('citas/', views.mis_citas, name='mis_citas'),
]