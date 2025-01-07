from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from stock.models import Product
from pages.models import BusinessType


@login_required
def pos(request):
    # Obtener el carrito de la sesión o una lista vacía si no existe
    cart = request.session.get('cart', [])
    
    # Calcular el total con Decimal para evitar problemas de punto flotante
    total_amount = sum(Decimal(str(item.get('total_price', 0))) for item in cart)
    
    # Obtener todos los productos del usuario
    products = Product.objects.filter(user=request.user).order_by('name')
    
    context = {
        'categories': BusinessType.objects.get(pk=request.user.business_type.id).category_list.all(),
        'products': products,
        'cart_items': cart,
        'total_amount': total_amount,
    }
    return render(request, 'pos/pos.html', context)
