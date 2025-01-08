from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from . import scipts
from .models import BusinessType


def home(request):
    return render(request, 'home.html')

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
    return render('pages/business_type_selection')