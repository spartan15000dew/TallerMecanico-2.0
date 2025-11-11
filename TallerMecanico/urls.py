"""
URL configuration for TallerMecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from aplicacionTaller import views

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls, name='admin'),

    # Autenticación
    path('login/', views.renderLogin, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Menú principal
    path('', views.rendermMenu, name='menu'),

    # Citas
    path('citas/', views.renderCitas, name='citas'),

    # Servicios
    path('servicios/', views.servicios_base, name='servicios_base'),
    path('servicios/cliente/', views.cliente, name='cliente'),
    path('servicios/administrador/', views.administrador, name='administrador'),
    path('servicios/mecanico/', views.mecanico, name='mecanico'),
]
