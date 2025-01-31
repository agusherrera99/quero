from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def plans(request):
    plans = [
        {
            "name": "Prueba Gratis",
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
    
    return render(request, 'plans.html', {'plans': plans})

def receive_contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_message = EmailMessage(
            subject='CONTACTO',
            body=f"""
            -- Mensaje de Contacto --

            **Nombre**: {name}
            **Correo Electrónico**: {request.user.email}
            **Teléfono**: {phone}

            **Asunto**: {subject}

            **Mensaje**:
            {message}

            -- Fin del Mensaje --
            """,
            from_email=email,
            to=[settings.EMAIL_HOST_USER],
        )
        email_message.reply_to = [request.user.email]

        try:
            email_message.send(fail_silently=False)
            messages.success(request, 'Gracias por contactarnos, te responderemos a la brevedad.')
        except Exception:
            messages.error(request, 'Ocurrió un error al enviar el mensaje.')
            
        return redirect('pages:home')