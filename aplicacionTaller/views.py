from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.utils import timezone


from .forms import (
    FormularioUsuario, 
    FormularioCliente, 
    FormularioMecanico,
    VehiculoForm,  
    CitaForm       
)

from .models import Vehiculo, Cita, Mecanico


def es_cliente(user):
    return user.groups.filter(name='Clientes').exists()

def es_mecanico(user):
    return user.groups.filter(name='Mecanicos').exists()

def es_admin(user):
    return user.is_staff or user.is_superuser




@transaction.atomic 
def registro_view(request):
    tipo_usuario_seleccionado = 'Cliente'
    
    user_form = FormularioUsuario()
    cliente_form = FormularioCliente(prefix="cliente")
    mecanico_form = FormularioMecanico(prefix="mecanico")

    if request.method == 'POST':
        tipo_usuario_seleccionado = request.POST.get('tipo_usuario')
        user_form = FormularioUsuario(request.POST)

        if tipo_usuario_seleccionado == 'Cliente':
            cliente_form = FormularioCliente(request.POST, prefix="cliente")
            
            if user_form.is_valid() and cliente_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                
                try:
                    grupo_clientes = Group.objects.get(name='Clientes')
                    user.groups.add(grupo_clientes)
                except Group.DoesNotExist:
                    messages.error(request, "Error interno: El grupo 'Clientes' no existe.")
                    return redirect('registro')

                cliente = cliente_form.save(commit=False)
                cliente.usuario = user 
                cliente.save()
                
                messages.success(request, 'Cliente registrado exitosamente. Por favor, inicie sesión.')
                return redirect('login')
            else:
                messages.error(request, 'Error al registrar el cliente. Por favor, revise los datos.')

        elif tipo_usuario_seleccionado == 'Mecanico':
            mecanico_form = FormularioMecanico(request.POST, prefix="mecanico")
            
            if user_form.is_valid() and mecanico_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                
                mecanico = mecanico_form.save(commit=False)
                mecanico.usuario = user 
                mecanico.save()
                mecanico_form.save_m2m() 
                
                messages.success(request, 'Mecánico registrado. Su cuenta está pendiente de aprobación por un administrador.')
                return redirect('login')
            else:
                messages.error(request, 'Error al registrar el mecánico. Por favor, revise los datos.')
        
        else:
            messages.error(request, 'Tipo de usuario no válido.')

    return render(request, 'registro.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'mecanico_form': mecanico_form,
        'tipo_usuario_seleccionado': tipo_usuario_seleccionado, 
    })


def renderLogin(request):
    if request.user.is_authenticated:
        return redirect('menu') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'perfil_mecanico') and not user.perfil_mecanico.aprobado:
                messages.error(request, "Su cuenta de mecánico aún no ha sido aprobada por un administrador.")
                return redirect('login')
            
            login(request, user)
            return redirect('menu') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')




def rendermMenu(request):
    contexto = {}
    user = request.user

    if hasattr(user, 'perfil_cliente'):
        contexto['rol'] = 'cliente'
    elif hasattr(user, 'perfil_mecanico'):
        contexto['rol'] = 'mecanico'
    elif user.is_superuser or user.is_staff:
        contexto['rol'] = 'administrador'
    else:
        contexto['rol'] = 'indefinido'

    return render(request,"menu.html", contexto)

@login_required
@user_passes_test(es_cliente)
def panel_cliente(request):
    """Panel principal del cliente. Muestra citas y vehículos."""
    perfil_cliente = request.user.perfil_cliente
    vehiculos = Vehiculo.objects.filter(cliente=perfil_cliente)
    citas = Cita.objects.filter(vehiculo__in=vehiculos).order_by('-fecha_hora')
    contexto = {
        'vehiculos': vehiculos,
        'citas': citas
    }
    return render(request, "servicios/panel_cliente.html", contexto)

@login_required
@user_passes_test(es_mecanico)
def panel_mecanico(request):
    """Panel principal del mecánico. Muestra citas pendientes y asignadas."""
    perfil_mecanico = request.user.perfil_mecanico
    
    citas_pendientes = Cita.objects.filter(estado='Pendiente').order_by('fecha_hora')
    
    citas_asignadas = Cita.objects.filter(
        mecanico_asignado=perfil_mecanico,
        estado__in=['Aprobada', 'En Progreso']
    ).order_by('fecha_hora')
    
    contexto = {
        'citas_pendientes': citas_pendientes,
        'citas_asignadas': citas_asignadas
    }
    return render(request, "servicios/panel_mecanico.html", contexto)

@login_required
@user_passes_test(es_admin)
def panel_administrador(request):
    """Panel principal del administrador."""
    mecanicos_pendientes = Mecanico.objects.filter(aprobado=False).count()
    contexto = {
        'mecanicos_pendientes': mecanicos_pendientes
    }
    return render(request, "servicios/panel_administrador.html", contexto)

def servicios_base(request):
    return render(request, "servicios/Base_servicios.html")




@login_required
@user_passes_test(es_cliente)
def gestionar_vehiculos(request):
    """Permite al cliente ver, añadir y editar sus vehículos."""
    perfil_cliente = request.user.perfil_cliente
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.cliente = perfil_cliente  
            vehiculo.save()
            messages.success(request, f"Vehículo {vehiculo.patente} registrado exitosamente.")
            return redirect('gestionar_vehiculos')
        else:
            messages.error(request, "Error al registrar el vehículo. Revise los datos.")
    else:
        form = VehiculoForm()

    vehiculos = Vehiculo.objects.filter(cliente=perfil_cliente)
    contexto = {
        'form': form,
        'mis_vehiculos': vehiculos
    }
    return render(request, 'servicios/gestionar_vehiculos.html', contexto)

@login_required
@user_passes_test(es_cliente)
def agendar_cita(request):
    """Formulario para que el cliente solicite una cita."""
    if request.method == 'POST':
        form = CitaForm(request.POST, user=request.user)
        if form.is_valid():
            cita = form.save(commit=False)
            if cita.fecha_hora < timezone.now():
                messages.error(request, "No puede agendar una cita en una fecha/hora pasada.")
            else:
                cita.estado = 'Pendiente' 
                cita.save()
                messages.success(request, "Su solicitud de cita ha sido enviada. Quedará pendiente de aprobación.")
                return redirect('panel_cliente')
        else:
            messages.error(request, "Error al agendar la cita. Revise los datos.")
    else:
        form = CitaForm(user=request.user)

    contexto = {
        'form': form
    }
    return render(request, 'servicios/agendar_cita.html', contexto)

@login_required
@user_passes_test(es_mecanico)
def detalle_cita_mecanico(request, pk):
    """Permite al mecánico ver detalles de una cita y aprobarla o rechazarla."""
    cita = get_object_or_404(Cita, pk=pk)
    perfil_mecanico = request.user.perfil_mecanico

    if request.method == 'POST':
        if 'accion_aprobar' in request.POST:
            cita.estado = 'Aprobada'
            cita.mecanico_asignado = perfil_mecanico
            cita.save()
            messages.success(request, f"Cita {cita.id} aprobada y asignada a usted.")
        
        elif 'accion_rechazar' in request.POST:
            cita.estado = 'Rechazada'
            cita.mecanico_asignado = None 
            cita.save()
            messages.warning(request, f"Cita {cita.id} ha sido rechazada.")
            
        elif 'accion_completar' in request.POST:
            cita.estado = 'Completada'
            cita.save()
            messages.success(request, f"Cita {cita.id} marcada como completada.")

        return redirect('panel_mecanico')

    contexto = {
        'cita': cita
    }
    return render(request, 'servicios/detalle_cita.html', contexto)




@login_required
def mis_citas(request):
    """Muestra citas según el rol del usuario."""
    contexto = {
        'es_cliente': False,
        'es_mecanico': False,
        'citas': Cita.objects.none() 
    }
    
    if hasattr(request.user, 'perfil_cliente'):
        contexto['es_cliente'] = True
        vehiculos_cliente = Vehiculo.objects.filter(cliente=request.user.perfil_cliente)
        contexto['citas'] = Cita.objects.filter(vehiculo__in=vehiculos_cliente).order_by('-fecha_hora')
        
    elif hasattr(request.user, 'perfil_mecanico'):
        contexto['es_mecanico'] = True
        citas_pendientes = Cita.objects.filter(estado='Pendiente')
        citas_propias = Cita.objects.filter(mecanico_asignado=request.user.perfil_mecanico)
        contexto['citas'] = (citas_pendientes | citas_propias).distinct().order_by('-fecha_hora')

    elif es_admin(request.user):
        contexto['citas'] = Cita.objects.all().order_by('-fecha_hora')

    return render(request, "mis_citas.html", contexto)