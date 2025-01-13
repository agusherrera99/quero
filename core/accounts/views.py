from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page

from .forms import UserLoginForm, UserRegistrationForm


@login_required
@cache_page(60 * 5)
def profile(request):
    return render(request, 'accounts/profile.html')

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
                
                return redirect('pages:business_type_selection')
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

