from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from . import scipts
from .forms import UserLoginForm, UserRegistrationForm
from account.models import BusinessType, Notification


@login_required
def profile(request):
    return render(request, 'account/profile.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = email.split('@')[0]
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Bienvenido, {user.username}!')
                    return redirect('pos:pos')
                else:
                    messages.error(request, "Tu cuenta está desactivada.")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario no válido. Revisa los campos.")
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # usa el método set_password de Django para encriptar la contraseña antes de guardar el usuario en la base de datos.
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
                login(request, user)
                
                return redirect('account:business_type_selection')
            except Exception as e:
                messages.error(request, f"Hubo un problema al registrar tu cuenta: {str(e)}")
        else:
            messages.error(request, "Formulario no válido. Revisa los campos.")
    
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)

@login_required
def business_type_selection(request):
    business_types = scipts.generate_business_types()
    
    context = {
        'business_types': business_types
    }
    return render(request, 'account/business_type_selection.html', context)

@login_required
@transaction.atomic
def select_business_type(request):
    if request.method == 'POST':
        business_type = request.POST.get('business_type')
        business_type_id = BusinessType.objects.get(name=business_type)
     
        request.user.business_type = business_type_id
        # Eliminar todos los productos del usuario
        request.user.product_set.all().delete()
        request.user.save()

        # Refrescar la instancia del usuario para evitar problemas con la caché
        request.user.refresh_from_db()

        messages.success(request, 'Tipo de negocio seleccionado con éxito.')
        return redirect('account:profile')
    return render('account/business_type_selection.html')

def mark_notification_as_read(request, notification_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Usuario no autenticado'}, status=401)

    try:
        # Obtener la notificación de la base de datos
        notification = Notification.objects.get(id=notification_id, user=request.user)

        # Marcarla como leída
        notification.mark_as_read()

        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notificación no encontrada'}, status=404)