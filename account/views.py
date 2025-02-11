from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from . import scripts
from .forms import UserLoginForm, UserRegistrationForm
from account.models import BusinessType, CustomUser, Notification


@login_required
def profile(request):
    sub_accounts = CustomUser.objects.filter(parent_account=request.user)

    context = {
        'sub_accounts': sub_accounts,
    }
    return render(request, 'account/profile.html', context)

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

@login_required
def delete_account(request):
    return render(request, 'account/delete_account.html')

def delete_subaccounts(user):
    sub_accounts = CustomUser.objects.filter(parent_account=user)
    try:
        for sub_account in sub_accounts:
            sub_account.product_set.all().delete()
            sub_account.spend_set.all().delete()
            sub_account.notifications.all().delete()
            sub_account.delete()
    except Exception as e:
        raise Exception(f"Hubo un problema al eliminar las subcuentas: {str(e)}")

@login_required
def delete_account_confirm(request):
    """
    Eliminar la cuenta de un usuario.
    
    Se eliminan todos los productos, gastos y notificaciones del usuario.
    Se eliminan todas las subcuentas asociadas al usuario.
    """
    if request.user.is_sub_account:
        messages.error(request, 'No tienes permiso para eliminar tu cuenta.')
        return redirect('account:profile')
    else:
        try:
            request.user.product_set.all().delete()
            request.user.spend_set.all().delete()
            request.user.notifications.all().delete()
            delete_subaccounts(request.user)
            request.user.delete()
            return redirect('pages:home')
        except Exception as e:
            messages.error(request, f"Hubo un problema al eliminar tu cuenta: {str(e)}")
        return redirect('account:profile')

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
def create_sub_account(request):
    return render(request, 'account/create_sub_account.html')

@login_required
def add_sub_account(request):
    """
    Agregar una subcuenta a un usuario principal.
    """
    if request.user.is_sub_account:
        messages.error(request, 'No tienes permiso para crear subcuentas.')
        return redirect('account:profile')
    else:
        if request.method == 'POST':
            first_name = request.POST.get('sub_account_first_name')
            last_name = request.POST.get('sub_account_last_name')
            sub_account_email = request.POST.get('sub_account_email')
            sub_account_username = request.POST.get('sub_account_username')
            sub_account_password = request.POST.get('sub_account_password')
            sub_account_password2 = request.POST.get('sub_account_password2')
            sub_account_phone = request.POST.get('sub_account_phone')

            if sub_account_password != sub_account_password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('account:create_sub_account')

            try:
                sub_account = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=sub_account_email,
                    username=sub_account_username,
                    password=sub_account_password,
                    phone=sub_account_phone,
                    shop_name=request.user.shop_name,
                    business_type=request.user.business_type,
                    tier=request.user.tier,
                    is_paid=request.user.is_paid,
                    payment_due=request.user.payment_due,
                    parent_account=request.user,
                    is_sub_account=True,
                )
                messages.success(request, f'Subcuenta {sub_account.username} creada con éxito.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al crear la subcuenta: {str(e)}')
            
            return redirect('account:profile')

@login_required
def delete_sub_account(request, sub_account_id):
    if request.user.is_sub_account:
        messages.error(request, 'No tienes permiso para eliminar subcuentas.')
        return redirect('account:profile')
    else:
        try:
            sub_account = CustomUser.objects.get(id=sub_account_id, parent_account=request.user)
            sub_account.delete()
            messages.success(request, f'Subcuenta {sub_account.username} eliminada con éxito.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Subcuenta no encontrada.')
        return redirect('account:profile')

@login_required
def support(request):
    return render(request, 'account/support.html')

@login_required
def receive_support_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_message = EmailMessage(
            subject='SOPORTE',
            body=f"""
            -- Mensaje de Soporte --

            **Nombre del Usuario**: {request.user.username}
            **Correo Electrónico**: {request.user.email}
            **Teléfono**: {request.user.phone}
            **Tier**: {request.user.tier.name}
            **Plan Pagado**: {request.user.is_paid}
            

            **Asunto**: {subject}

            **Mensaje**:
            {message}

            -- Fin del Mensaje --
            """,
            from_email=request.user.email,
            to=[settings.EMAIL_HOST_USER],
        )
        email_message.reply_to = [request.user.email]

        try:
            email_message.send(fail_silently=False)
            messages.success(request, 'Gracias por contactarnos, te responderemos a la brevedad.')
        except Exception:
            messages.error(request, 'Ocurrió un error al enviar el mensaje.')
            
        return redirect('pos:pos')

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
        
        if business_type_id is None:
            messages.error(request, 'Tipo de negocio no válido.')
            return redirect('account:business_type_selection')
        elif request.user.business_type == business_type_id:
            messages.info(request, 'Actualmente tienes seleccionado este tipo de negocio.')
            return redirect('account:business_type_selection')


        request.user.business_type = business_type_id
        # Eliminar todos los productos, gastos y notificaciones del usuario
        request.user.product_set.all().delete()
        request.user.spend_set.all().delete()
        request.user.notifications.all().delete()
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