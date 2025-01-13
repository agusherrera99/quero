from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import redirect, render

from . import scipts
from .models import BusinessType


def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def receive_contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_message = EmailMessage(
            subject=f'Nuevo mensaje de {name} - Asunto: {subject}',
            body=f'Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}',
            from_email=email,
            to=[settings.EMAIL_HOST_USER],
        )

        try:
            email_message.send(fail_silently=False)
            messages.success(request, 'Gracias por contactarnos, te responderemos a la brevedad.')
        except Exception:
            messages.error(request, 'Ocurrió un error al enviar el mensaje.')
            
        return redirect('pages:contact')

@login_required
def business_type_selection(request):
    business_types = scipts.generate_business_types()
    
    context = {
        'business_types': business_types
    }
    return render(request, 'pages/business_type_selection.html', context)

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

        messages.success(request, 'Tipo de negocio seleccionado con éxito.')
        return redirect('accounts:profile')
    return render('pages/business_type_selection.html')