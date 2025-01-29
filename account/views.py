from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from . import scripts
from .forms import UserLoginForm, UserRegistrationForm
from account.models import BusinessType, CustomUser, Notification


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
                try:
                    custom_user = CustomUser.objects.get(email=email)
                    if not custom_user.is_active:
                        messages.error(request, "Tu cuenta ha sido desactivada. Contacta al administrador.")
                    else:
                        messages.error(request, "Usuario o Contraseña incorrecta.")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Este usuario no existe. Por favor, regístrate.")
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
    business_types = scripts.generate_business_types()
    
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

@login_required
def update_plan(request):

    user_tier = request.user.tier if hasattr(request.user, 'tier') else None

    tiers = [
        {
            "name": "Prueba Gratuita",
            "free": True,
            "monthly_price": None,
            "annual_price": None,
            "one_time_price": None,
            "discount": None,
            "description": "Prueba nuestra plataforma sin compromiso",
            "features": [
                "Acceso por 15 días",
            ],
        },
        {
            "name": "Plan Mensual",
            "free": False,
            "monthly_price": 14.99,
            "annual_price": None,
            "one_time_price": None,
            "discount": None,
            "description": "Flexibilidad mensual para tus necesidades",
            "features": [
                "Acceso completo",
                "Soporte a demanda",
                "Accesso a nuevas funciones, en cuanto estén disponibles",
            ],
        },
        {
            "name": "Plan Anual",
            "free": False,
            "monthly_price": 12.49,
            "annual_price": 149.99,
            "one_time_price": None,
            "discount": 16,
            "description": "Ahorra con nuestro plan anual",
            "features": [
                "Todo lo del plan mensual",
                "Soporte prioritario",
                "Acceso anticipado a nuevas funciones",
            ],
        },
        {
            "name": "Pago único, para siempre",
            "free": False,
            "monthly_price": None,
            "annual_price": None,
            "one_time_price": 1199.99,
            "discount": 33.3,
            "description": "Acceso de por vida con un solo pago",
            "features": [
                "Todo lo del plan anual",
                "Acceso ilimitado de por vida",
                "Soporte vitalicio",
                "Acceso a funciones exclusivas",
            ],
        },
    ]
    return render(request, 'account/update_plan.html', {'tiers': tiers, 'user_tier': user_tier})

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