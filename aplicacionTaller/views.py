from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import FormularioUsuario, FormularioCliente, FormularioMecanico

#VISTA DE REGISTRO
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
            mecanico_form = FormularioMecanico(prefix="mecanico") 
            
            if user_form.is_valid() and cliente_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                cliente = cliente_form.save(commit=False)
                cliente.usuario = user
                cliente.save()
                messages.success(request, 'Cliente registrado exitosamente. Por favor, inicie sesión.')
                return redirect('login')
            else:
                if not user_form.is_valid(): print("Errores User Form:", user_form.errors)
                if not cliente_form.is_valid(): print("Errores Cliente Form:", cliente_form.errors)
                
                if not user_form.is_valid():
                    for field, errors in user_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Usuario - {field}: {error}")
                if not cliente_form.is_valid():
                     for field, errors in cliente_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Cliente - {field}: {error}")
                messages.error(request, 'Error al registrar el cliente. Por favor, revise los datos.')

        elif tipo_usuario_seleccionado == 'Mecanico':
            
            mecanico_form = FormularioMecanico(request.POST, prefix="mecanico")
            cliente_form = FormularioCliente(prefix="cliente")
            
            if user_form.is_valid() and mecanico_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                mecanico = mecanico_form.save(commit=False)
                mecanico.usuario = user
                mecanico.save()
                messages.success(request, 'Mecánico registrado exitosamente. Por favor, inicie sesión.')
                return redirect('login')
            else:
                if not user_form.is_valid(): print("Errores User Form:", user_form.errors)
                if not mecanico_form.is_valid(): print("Errores Mecanico Form:", mecanico_form.errors)
                
                if not user_form.is_valid():
                    for field, errors in user_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Usuario - {field}: {error}")
                if not mecanico_form.is_valid():
                    for field, errors in mecanico_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Mecanico - {field}: {error}")
                messages.error(request, 'Error al registrar el mecánico. Por favor, revise los datos.')
        
        else:
            messages.error(request, 'Tipo de usuario no válido.')
            cliente_form = FormularioCliente(prefix="cliente")
            mecanico_form = FormularioMecanico(prefix="mecanico")

    return render(request, 'registro.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'mecanico_form': mecanico_form,
        'tipo_usuario_seleccionado': tipo_usuario_seleccionado, 
    })


#VISTA DE LOGIN
def renderLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'login.html')

#VISTA DE MENÚ
def rendermMenu(request):
    contexto = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'perfil_cliente'):
            contexto['rol'] = 'cliente'
            contexto['perfil'] = request.user.perfil_cliente
        elif hasattr(request.user, 'perfil_mecanico'):
            contexto['rol'] = 'mecanico'
            contexto['perfil'] = request.user.perfil_mecanico
        else:
            contexto['rol'] = 'administrador'
    else:
        return redirect('login') 
    return render(request,"menu.html", contexto)

#VISTA DE LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

#OTRAS VISTAS ESTÁTICAS
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