from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import FormularioUsuario, FormularioCliente, FormularioMecanico
from django.db import transaction 


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
            
            # Si pasa la verificación (es cliente, admin, o mecánico aprobado)
            login(request, user)
            return redirect('menu') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            
    return render(request, 'login.html')

#VISTA DE MENÚ (ACTUALIZADA PARA ROLES)
def rendermMenu(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    contexto = {}
    user = request.user

    # Identificar el rol del usuario
    if hasattr(user, 'perfil_cliente'):
        contexto['rol'] = 'cliente'
        contexto['perfil'] = user.perfil_cliente
    elif hasattr(user, 'perfil_mecanico'):

        contexto['rol'] = 'mecanico'
        contexto['perfil'] = user.perfil_mecanico
    elif user.is_superuser or user.is_staff:
        contexto['rol'] = 'administrador'
    else:

        contexto['rol'] = 'indefinido'
        messages.warning(request, "Su cuenta no tiene un perfil asignado.")

    return render(request,"menu.html", contexto)


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


def renderCitas(request):
    return render(request,"citas.html")
def servicios_base(request):
    return render(request, "servicios/Base_servicios.html")
def cliente(request):
    return render(request, "servicios/Cliente_servicios.html")
def administrador(request):
    return render(request, "servicios/Administrador_servicios.html")
def mecanico(request):
    return render(request, "servicios/Mecanico_servicios.html")