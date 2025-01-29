import json

from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import redirect, render

from stock.models import Product
from .models import Sale


@login_required
def pos(request):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', [])
    
    # Calcular el total de la compra
    total_amount = sum(Decimal(item.get('total_price', 0)) for item in cart)
    
    # Obtener todos los productos del usuario
    products = Product.objects.filter(user=request.user).select_related('subcategory__category').order_by('name')

    business_type = request.user.business_type
    
    categories = cache.get('cart_categories')
    if not categories:
        categories = business_type.category_list.all()
        cache.set('cart_categories', categories)

    context = {
        'categories': categories,
        'products': products,
        'cart_items': cart,
        'total_amount': total_amount,
    }
    return render(request, 'pos.html', context)

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

        return render(request, 'sales_confirmation.html', context)
    else:
        messages.error(request, 'No se ha recibido el carrito de la compra')
        return redirect('pos:pos')

@login_required
@transaction.atomic
def process_sale(request):
    # Obtener el carrito y la fecha del POST
    cart_json = request.POST.get('cart', [])

    if not cart_json:
        messages.error(request, 'No se ha recibido el carrito de la compra')
        return redirect('pos:pos')

    # Guardar venta en la base de datos y actualizar el stock
    cart_json = cart_json.replace("'", '"')
    cart = json.loads(cart_json)
    for item in cart:
        product = Product.objects.get(pk=item.get('product_id'))

        if request.user != product.user:
            messages.error(request, 'No puedes vender productos que no te pertenecen')
            return redirect('pos:pos')
        
        
        quantity = Decimal(item.get('quantity', 0)) 
        total_price = Decimal(item.get('total_price', 0))

        if quantity <= 0:
            messages.error(request, 'La cantidad no puede ser negativa')
            return redirect('pos:pos')

        errors = []
        if request.user != product.user:
            errors.append('No puedes vender productos que no te pertenecen')
        if quantity <= 0:
            errors.append('La cantidad no puede ser negativa')
        if product.quantity < quantity:
            errors.append(f'No hay suficiente stock para el producto {product.name}')

        # Verificar la unidad de medida y ajustar el cálculo del precio total
        if product.uom == 'unidad':
            total_price = product.price * quantity
        elif product.uom == 'kilogramo' or product.uom == 'litro':
            total_price = product.price * Decimal(quantity)
        elif product.uom == 'gramo' or product.uom == 'mililitro':
            total_price = product.price * (Decimal(quantity) / 1000)
        else:
            messages.error(request, 'Unidad de medida no válida')
            return redirect('pos:pos')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('pos:pos')

        # Crear la venta y guardarla en la base de datos
        sale = Sale(product=product, quantity=quantity, total_price=total_price, user=request.user)
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
    messages.info(request, 'Venta cancelada correctamente')
    return redirect('pos:pos')
