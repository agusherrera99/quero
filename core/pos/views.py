import json

from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from stock.models import Product
from pages.models import BusinessType
from .models import Sale


@login_required
def pos(request):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', [])
    
    # Calcular el total de la compra
    total_amount = sum(Decimal(item.get('total_price', 0)) for item in cart)
    
    # Obtener todos los productos del usuario
    products = Product.objects.filter(user=request.user).order_by('name')
    
    context = {
        'categories': BusinessType.objects.get(pk=request.user.business_type.id).category_list.all(),
        'products': products,
        'cart_items': cart,
        'total_amount': total_amount,
    }
    return render(request, 'pos/pos.html', context)

@login_required
def sales_confirmation(request):
    if request.method == 'POST':
        cart_json = request.POST.get('cart')
        if not cart_json:
            messages.error(request, 'No se ha recibido el carrito de la compra correctamente')
            return redirect('pos:pos')

        total_amount = request.POST.get('total_amount', 0)
        cart = json.loads(cart_json)
        total_amount = Decimal(total_amount)

        current_datetime = datetime.now()

        context = {
            'cart_items': cart,
            'total_amount': total_amount,
            'current_datetime': current_datetime,
        }

        return render(request, 'pos/sales_confirmation.html', context)
    else:
        messages.error(request, 'No se ha recibido el carrito de la compra')
        return redirect('pos:pos')

@login_required
@transaction.atomic
def process_sale(request):
    # Obtener el carrito y la fecha del POST
    cart_json = request.POST.get('cart', [])
    current_datetime = request.POST.get('current_datetime', None)

    if not cart_json:
        messages.error(request, 'No se ha recibido el carrito de la compra')
        return redirect('pos:pos')

    if not current_datetime:
        current_datetime = datetime.now()

    # Guardar venta en la base de datos y actualizar el stock
    cart_json = cart_json.replace("'", '"')
    cart = json.loads(cart_json)
    for item in cart:
        product = Product.objects.get(pk=item.get('product_id'))

        if request.user != product.user:
            messages.error(request, 'No puedes vender productos que no te pertenecen')
            return redirect('pos:pos')
        
        quantity = item.get('quantity', 0)
        quantity = int(quantity)

        if quantity <= 0:
            messages.error(request, 'La cantidad no puede ser negativa')
            return redirect('pos:pos')

        # Validar que haya suficiente stock
        if product.quantity < quantity:
            messages.error(request, 'No hay suficiente stock para el producto ' + product.name)
            return redirect('pos:pos')
        
        total_price = item.get('price', 0)

        # Crear la venta y guardarla en la base de datos
        sale = Sale(
            product=product,
            quantity=quantity,
            created_at=current_datetime,
            total_price=total_price,
            user=request.user
        )
        print(sale)
        sale.save()
        
        # Actualizar el stock del producto
        product.quantity -= quantity
        product.save()

    # Limpiar el carrito
    request.session['cart'] = []

    messages.success(request, 'Venta realizada correctamente')
    return redirect('pos:pos')

@login_required
def cancel_sale(request):
    # Limpiar el carrito de la sesión
    if 'cart' in request.session:
        request.session['cart'] = []
    messages.success(request, 'Venta cancelada correctamente')
    return redirect('pos:pos')
