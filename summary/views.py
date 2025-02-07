from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, F, IntegerField, Sum, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from pos.models import Sale
from .forms import SalesForm

def calculate_percentage_change(current, previous):
    if previous is None or previous == 0:
        return None, 'No disponible', 'gray'

    if current is None:
        current = 0
    
    percentage_change = ((current - previous) / previous) * 100
    if percentage_change < 0:
        return abs(percentage_change), f"{abs(percentage_change):.2f}%", 'red'
    elif percentage_change == 0:
        return 0, "Igual", "gray"
    else:
        return percentage_change, f"{percentage_change:.2f}%", 'green'
    
def get_sales_data_for_period(period):
    cache_key = f"sales_data_{period}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    today = datetime.today()
    start_date = today - timedelta(days=period)

    # Usar una consulta agregada con `values` y `annotate` más eficiente
    sales_data = Sale.objects.filter(created_at__date__gte=start_date).values(
        'created_at__date'
    ).annotate(
        total_sales=Sum('total_price')
    ).order_by('created_at__date')

    sales_dates = [entry['created_at__date'].strftime('%Y-%m-%d') for entry in sales_data]
    sales_values = [entry['total_sales'] for entry in sales_data]

    result = {'dates': sales_dates, 'values': sales_values}
    cache.set(cache_key, result, 60)
    return result

@login_required
def sales_data(request):
    period = request.GET.get('period', 7)
    period = int(period[:-1])

    data = get_sales_data_for_period(period)
    
    return JsonResponse(data)

def get_category_sales_data():
    cache_key = "category_sales_data"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    category_sales = Sale.objects.values(
        category_name=F('product__subcategory__category__name')
    ).annotate(
        total_sales=Sum('total_price')
    ).order_by('-total_sales')

    category_labels = [entry['category_name'] for entry in category_sales]
    category_values = [entry['total_sales'] for entry in category_sales]

    result = {'labels': category_labels, 'values': category_values}
    cache.set(cache_key, result, 60)
    return result

def get_subcategory_sales_data():
    cache_key = "subcategory_sales_data"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    subcategory_sales = Sale.objects.values(
        subcategory_name=F('product__subcategory__name')
    ).annotate(
        total_sales=Sum('total_price')
    ).order_by('-total_sales')

    subcategory_labels = [entry['subcategory_name'] for entry in subcategory_sales]
    subcategory_values = [entry['total_sales'] for entry in subcategory_sales]

    result = {'labels': subcategory_labels, 'values': subcategory_values}
    cache.set(cache_key, result, 60)
    return result

@login_required
def category_sales_data(request):
    data = get_category_sales_data()
    return JsonResponse(data)

@login_required
def subcategory_sales_data(request):
    data = get_subcategory_sales_data()
    return JsonResponse(data)

@login_required
def summary(request):
    # Obtener las ventas del usuario
    sales = Sale.objects.filter(user=request.user).select_related('product__subcategory__category').order_by('-created_at')

    # Calcula el primer día del mes actual y el día anterior
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    yesterday = today - timedelta(days=1)
    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

    # Ventas Totales de hoy y ayer
    daily_sales_data = sales.aggregate(
        total_sales_today=Sum(Case(
            When(created_at__date=today, then='total_price'),
            default=Value(0),
            output_field=IntegerField()
        )),
        total_sales_yesterday=Sum(Case(
            When(created_at__date=yesterday, then='total_price'),
            default=Value(0),
            output_field=IntegerField()
        ))
    )
    daily_sales = daily_sales_data.get('total_sales_today', 0) if daily_sales_data else 0
    daily_sales_yesterday = daily_sales_data.get('total_sales_yesterday', 0) if daily_sales_data else 0
    daily_sales_percentage, daily_sales_percentage_text, daily_sales_percentage_color = calculate_percentage_change(daily_sales, daily_sales_yesterday)

    # Productos vendidos (Hoy)
    daily_products_sold_data = sales.aggregate(
        total_quantity_today=Sum(Case(
            When(created_at__date=today, then='quantity'),
            default=Value(0),
            output_field=IntegerField()
        )),
        total_quantity_yesterday=Sum(Case(
            When(created_at__date=yesterday, then='quantity'),
            default=Value(0),
            output_field=IntegerField()
        ))
    )

    daily_products_sold = daily_products_sold_data.get('total_quantity_today', 0) if daily_products_sold_data else 0
    if daily_products_sold is not None:
        daily_products_sold = round(daily_products_sold)
    else: 
        daily_products_sold = 0

    daily_products_sold_yesterday = daily_products_sold_data.get('total_quantity_yesterday', 0) if daily_products_sold_data else 0
    if daily_products_sold_yesterday is not None:
        daily_products_sold_yesterday = round(daily_products_sold_yesterday)
    else:
        daily_products_sold_yesterday = 0
        
    daily_products_sold_percentage, daily_products_sold_percentage_text, daily_products_sold_percentage_color = calculate_percentage_change(daily_products_sold, daily_products_sold_yesterday)

    # Ventas Totales (Mes)
    monthly_sales = sales.filter(created_at__date__gte=first_day_current_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    monthly_sales_last_month = sales.filter(created_at__date__gte=first_day_last_month, created_at__date__lt=first_day_current_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    monthly_sales_percentage, monthly_sales_percentage_text, monthly_sales_percentage_color = calculate_percentage_change(monthly_sales, monthly_sales_last_month)

    # Productos vendidos (Mes)
    monthly_products_sold = sales.filter(created_at__date__gte=first_day_current_month).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    if monthly_products_sold is not None:
        monthly_products_sold = round(monthly_products_sold)
    else:
        monthly_products_sold = 0
        
    monthly_products_sold_last_month = sales.filter(created_at__date__gte=first_day_last_month, created_at__date__lt=first_day_current_month).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    monthly_products_sold_last_month = round(monthly_products_sold_last_month)
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
        ).filter(search__icontains=sale_query)

    # Si no hay búsqueda, simplemente paginamos las ventas
    sales_paginator = Paginator(sales_results if sales_results else sales, 10)
    page_number = request.GET.get('page', 1)
    sales = sales_paginator.get_page(page_number)

    # Agrupar por 'product_id' para que las ventas de un mismo producto se sumen correctamente
    top_sales = Sale.objects.values('product__id', 'product__name', 'product__subcategory__category__name', 'product__uom')\
        .annotate(
            total_quantity=Sum('quantity'),
            total_price=Sum('total_price')  # Sumar el total de dinero por cada producto
        )\
        .filter(user=request.user)\
        .order_by('-total_price')[:10]
    
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

    return render(request, 'summary.html', context)

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
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('summary:summary')

    context = {
        'sale': sale
    }
    return render(request, 'delete_sale.html', context)
