from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from pos.models import Sale
from .forms import SalesForm

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
def summary(request):
    # Obtener las ventas del usuario
    sales = Sale.objects.filter(user=request.user).order_by('-created_at')

    # Calcula el primer día del mes actual y el día anterior
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    yesterday = today - timedelta(days=1)
    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

    # Ventas Totales (Hoy)
    daily_sales = sales.filter(created_at__date=today).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    daily_sales_yesterday = sales.filter(created_at__date=yesterday).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    daily_sales_percentage, daily_sales_percentage_text, daily_sales_percentage_color = calculate_percentage_change(daily_sales, daily_sales_yesterday)

    # Productos vendidos (Hoy)
    daily_products_sold = sales.filter(created_at__date=today).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    daily_products_sold_yesterday = sales.filter(created_at__date=yesterday).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    daily_products_sold_percentage, daily_products_sold_percentage_text, daily_products_sold_percentage_color = calculate_percentage_change(daily_products_sold, daily_products_sold_yesterday)

    # Ventas Totales (Mes)
    monthly_sales = sales.filter(created_at__date__gte=first_day_current_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    monthly_sales_last_month = sales.filter(created_at__date__gte=first_day_last_month, created_at__date__lt=first_day_current_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    monthly_sales_percentage, monthly_sales_percentage_text, monthly_sales_percentage_color = calculate_percentage_change(monthly_sales, monthly_sales_last_month)

    # Productos vendidos (Mes)
    monthly_products_sold = sales.filter(created_at__date__gte=first_day_current_month).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    monthly_products_sold_last_month = sales.filter(created_at__date__gte=first_day_last_month, created_at__date__lt=first_day_current_month).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    monthly_products_sold_percentage, monthly_products_sold_percentage_text, monthly_products_sold_percentage_color = calculate_percentage_change(monthly_products_sold, monthly_products_sold_last_month)
    
    # Buscador de ventas
    sale_search_form = SalesForm()
    sale_query = None
    sales_results = []

    if 'sale_query' in request.GET:
        # Usar SearchVector para la búsqueda de texto completo en el nombre del producto
        sale_search_form = SalesForm(request.GET)
        if sale_search_form.is_valid():
            sale_query = sale_search_form.cleaned_data['sale_query']
            sales_results = sales.annotate(
            search=SearchVector('product__name')
        ).filter(search=sale_query)

    # Si no hay búsqueda, simplemente paginamos las ventas
    if not sales_results:
        # Paginación de Ventas (también debes realizar la paginación sobre sales si no hay filtro de búsqueda)
        sales_paginator = Paginator(sales, 10)
        page_number = request.GET.get('page')
        sales = sales_paginator.get_page(page_number)
    else:
        # Paginamos los resultados de búsqueda si los hay
        sales_paginator = Paginator(sales_results, 10)
        page_number = request.GET.get('page')
        sales_results = sales_paginator.get_page(page_number)


    # Agrupar por 'product_id' para que las ventas de un mismo producto se sumen correctamente
    top_sales = Sale.objects.values('product__id', 'product__name', 'product__subcategory__category__name')\
        .annotate(
            total_quantity=Sum('quantity'),
            total_price=Sum('total_price')  # Sumar el total de dinero por cada producto
        )\
        .filter(user=request.user)\
        .order_by('-total_quantity')[:10]
    
    # Paginación de los productos más vendidos
    top_sales_paginator = Paginator(top_sales, 10)
    page_number = request.GET.get('page')
    top_sales = top_sales_paginator.get_page(page_number)

    context = {
        'daily_sales': daily_sales,
        'daily_sales_percentage': daily_sales_percentage,
        'daily_sales_percentage_text': daily_sales_percentage_text,
        'daily_sales_percentage_color': daily_sales_percentage_color,

        'daily_products_sold': daily_products_sold,
        'daily_products_sold_percentage': daily_products_sold_percentage,
        'daily_products_sold_percentage_text': daily_products_sold_percentage_text,
        'daily_products_sold_percentage_color': daily_products_sold_percentage_color,

        'monthly_sales': monthly_sales,
        'monthly_sales_percentage': monthly_sales_percentage,
        'monthly_sales_percentage_text': monthly_sales_percentage_text,
        'monthly_sales_percentage_color': monthly_sales_percentage_color,

        'monthly_products_sold': monthly_products_sold,
        'monthly_products_sold_percentage': monthly_products_sold_percentage,
        'monthly_products_sold_percentage_text': monthly_products_sold_percentage_text,
        'monthly_products_sold_percentage_color': monthly_products_sold_percentage_color,

        'sales': sales,  
        'sales_results': sales_results, 
        'sale_search_form': sale_search_form,
        'sale_query': sale_query, 
        'top_sales': top_sales
    }

    return render(request, 'summary/summary.html', context)

@login_required
@transaction.atomic
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if sale.user != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta venta.')
        return redirect('stock:stock')

    if request.method == 'POST':
        sale.delete()

        # Actualizar el stock del producto
        product = sale.product
        product.quantity += sale.quantity
        product.save()
        messages.info(request, 'Producto eliminado correctamente.')
        return redirect('summary:summary')

    context = {
        'sale': sale
    }
    return render(request, 'summary/delete_sale.html', context)
