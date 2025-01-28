from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddProductForm, SearchForm
from .models import Product, Subcategory
from pos.models import Sale


def calculate_percentage_change(current, previous):
    if previous is None or previous == 0:
        return None, 'No disponible', 'gray'
    
    percentage_change = ((current - previous) / previous) * 100
    if percentage_change < 0:
        return abs(percentage_change), f"{abs(percentage_change):.2f}%", 'red'
    elif percentage_change == 0:
        return 0, "Igual", "gray"
    else:
        return percentage_change, f"{percentage_change:.2f}%", 'green'

@login_required
def stock(request):
    products = Product.objects.filter(user=request.user).select_related('subcategory__category').order_by('-updated_at')

    # Fecha actual, primer día del mes actual y primer día del mes anterior
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

    # Productos creados en el mes actual y en el mes anterior
    current_month_products = products.filter(
        created_at__gte=first_day_current_month
    )
    last_month_products = products.filter(
        created_at__gte=first_day_last_month,
        created_at__lt=first_day_current_month
    )

    # Valores de stock para el mes actual y el mes anterior
    current_month_stock_value = current_month_products.aggregate(stock_value=Sum(F('quantity') * F('price')))['stock_value'] or 0
    last_month_stock_value = last_month_products.aggregate(stock_value=Sum(F('quantity') * F('price')))['stock_value'] or 0

    # Calcular el porcentaje de cambio
    unique_products_percentage, unique_products_percentage_text, unique_products_percentage_color = calculate_percentage_change(current_month_products.count(), last_month_products.count())
    total_quantity_percentage, total_quantity_percentage_text, total_quantity_percentage_color = calculate_percentage_change(current_month_products.aggregate(total_quantity=Sum('quantity'))['total_quantity'], last_month_products.aggregate(total_quantity=Sum('quantity'))['total_quantity'])
    stock_percentage, stock_percentage_text, stock_percentage_color = calculate_percentage_change(current_month_stock_value, last_month_stock_value)

    # Productos únicos, cantidad total y valor total de stock
    unique_products = products.values('name').distinct().count()
    total_quantity = products.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    stock_value = products.aggregate(stock_value=Sum(F('quantity') * F('price'))).get('stock_value', 0)
    stock_value = stock_value if stock_value is not None else 0

    # Formatear el valor del stock en formato argentino
    stock_formatted_value = "{:,.2f}".format(stock_value).replace(",", "X").replace(".", ",").replace("X", ".")

    # Buscador de productos
    search_form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = (
                products.annotate(search=SearchVector('name')).filter(search__icontains=query)
            )

    if not results:
        # Paginación de Ventas (también debes realizar la paginación sobre sales si no hay filtro de búsqueda)
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page', 1)
        products = paginator.get_page(page_number)
    else:
        # Paginamos los resultados de búsqueda si los hay
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page', 1)
        results = paginator.get_page(page_number)

    context = {
        'unique_products': unique_products,
        'unique_products_percentage': unique_products_percentage,
        'unique_products_percentage_text': unique_products_percentage_text,
        'unique_products_percentage_color': unique_products_percentage_color,

        'total_quantity': total_quantity,
        'total_quantity_percentage': total_quantity_percentage,
        'total_quantity_percentage_text': total_quantity_percentage_text,
        'total_quantity_percentage_color': total_quantity_percentage_color,

        'stock_formatted_value': stock_formatted_value,
        'stock_percentage': stock_percentage,
        'stock_percentage_text': stock_percentage_text,
        'stock_percentage_color': stock_percentage_color,

        'products': products,
        'search_form': search_form,
        'query': query,
        'results': results
    }

    return render(request, 'stock.html', context)

@login_required
@transaction.atomic
def add_stock(request):
    if request.method == 'POST':
        form = AddProductForm(data=request.POST, request=request)

        if form.is_valid():
            action = request.POST.get('action')

            if action == 'add_and_finish':
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity')
                price = form.cleaned_data.get('price')
                uom = form.cleaned_data.get('uom')
                subcategory = form.cleaned_data.get('subcategory')

                product = Product(
                    name=name,
                    quantity=quantity,
                    price=price,
                    uom=uom,
                    subcategory=subcategory,
                    user=request.user
                )
                product.save()
                messages.success(request, 'Producto añadido correctamente.')
                return redirect('stock:stock')
            elif action == 'add_and_continue':
                name = form.cleaned_data.get('name')
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity')
                price = form.cleaned_data.get('price')
                uom = form.cleaned_data.get('uom')
                subcategory = form.cleaned_data.get('subcategory')

                product = Product(
                    name=name,
                    quantity=quantity,
                    price=price,
                    uom=uom,
                    subcategory=subcategory,
                    user=request.user
                )
                product.save()
                return redirect('stock:add_stock')
        else:
            messages.error(request, 'Formulario no válido. Revisa los campos.')
    else:
        form = AddProductForm(request=request)
    
    context = {
        'form': form
    }
    return render(request, 'add_stock.html', context)

@login_required
@transaction.atomic
def edit_stock(request, pk):
    product = Product.objects.filter(pk=pk).select_related('subcategory__category').first()

    if product.user != request.user:
        messages.error(request, 'No tienes permisos para editar este producto.')
        return redirect('stock:stock')

    if request.method == 'POST':
        form = AddProductForm(data=request.POST, instance=product, request=request)
        if form.is_valid():
            form.save()
            messages.info(request, 'Producto actualizado correctamente.')
            return redirect('stock:stock')
        else:
            messages.error(request, 'Formulario no válido. Revisa los campos.')
    else:
        form = AddProductForm(instance=product, request=request)

    context = {
        'form': form,
    }
    return render(request, 'edit_stock.html', context)

@login_required
@transaction.atomic
def delete_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.user != request.user:
        messages.error(request, 'No tienes permisos para eliminar este producto.')
        return redirect('stock:stock')
    
    if request.method == 'POST':
        # Eliminar ventas asociadas al producto
        sale = Sale.objects.filter(product=product)
        sale.delete()

        product.delete()
        messages.info(request, 'Producto eliminado correctamente.')
        return redirect('stock:stock')

    context = {
        'product': product
    }
    return render(request, 'delete_stock.html', context)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')

    # Creamos un diccionario con las subcategorías que vamos a devolver
    subcategory_data = [{"id": subcategory.id, "name": subcategory.name} for subcategory in subcategories]
    return JsonResponse({"subcategories": subcategory_data})