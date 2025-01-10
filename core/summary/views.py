from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

import plotly.graph_objs as go

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
    
def get_sales_data_for_period(sales, perios):
    today = datetime.today()

    if perios == '7D':
        start_date = today - timedelta(days=7)
    elif perios == '30D':
        start_date = today - timedelta(days=30)
    elif perios == '90D':
        start_date = today - timedelta(days=90)
    elif perios == '1Y':
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=7) # Default: 7D

    # Agrupar ventas por fecha
    sales_data = sales.filter(created_at__gte=start_date)\
        .values('created_at__date')\
        .annotate(total_sales=Sum('total_price'))\
        .order_by('created_at')
    
    # Preparar los datos para el gráfico
    sales_dates = [sale['created_at__date'] for sale in sales_data][:100]
    sales_values = [sale['total_sales'] for sale in sales_data][:100]

    return sales_dates, sales_values
    

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
    
    # Gráfico de Ventas por Categoría (Pie Chart)
    # Ventas totales por Categoría
    category_sales = Sale.objects.values('product__subcategory__category__name')\
        .annotate(total_sales=Sum('total_price'))\
        .filter(user=request.user)\
        .order_by('-total_sales')
    
    category_sales_labels = [category['product__subcategory__category__name'] for category in category_sales]
    category_sales_values = [category['total_sales'] for category in category_sales]

    category_pie = go.Pie(
        labels=category_sales_labels,
        values=category_sales_values,
        name='Ventas por Categoría',
        hole=0.3
    )

    category_layout = go.Layout(
        title='Ventas por Categoría',
        showlegend=True,
        autosize=True
    )
    category_fig = go.Figure(data=[category_pie], layout=category_layout)
    category_graph_html = category_fig.to_html(full_html=False)

    # Gráfico de Ventas por Subcategoría (Pie Chart)
    # Ventas totales por Subcategoría
    subcategory_sales = Sale.objects.values('product__subcategory__name')\
        .annotate(total_sales=Sum('total_price'))\
        .filter(user=request.user)\
        .order_by('-total_sales')
    
    subcategory_sales_labels = [subcategory['product__subcategory__name'] for subcategory in subcategory_sales]
    subcategory_sales_values = [subcategory['total_sales'] for subcategory in subcategory_sales]

    subcategory_pie = go.Pie(
        labels=subcategory_sales_labels,
        values=subcategory_sales_values,
        name='Ventas por Subcategoría',
        hole=0.3
    )

    subcategory_layout = go.Layout(
        title='Ventas por Subcategoría',
        showlegend=True,
        autosize=True
    )
    subcategory_fig = go.Figure(data=[subcategory_pie], layout=subcategory_layout)
    subcategory_graph_html = subcategory_fig.to_html(full_html=False)

    # Obtener los datos de ventas para el gráfico de series temporales
    daily_sales_date, daily_sales_values = get_sales_data_for_period(sales, '7D')
    monthly_sales_date, monthly_sales_values = get_sales_data_for_period(sales, '30D')
    quarterly_sales_date, quarterly_sales_values = get_sales_data_for_period(sales, '90D')
    yearly_sales_date, yearly_sales_values = get_sales_data_for_period(sales, '1Y')

    # Gráfico de Ventas Diarias
    daily_series_chart = go.Figure()
    daily_series_chart.add_trace(
        go.Scatter(
            x=daily_sales_date,
            y=daily_sales_values,
            mode='lines+markers',
            name='Ventas Diarias',
        )
    )
    daily_series_chart.update_layout(
        title='Ventas Diarias',
        xaxis_title='Fecha',
        yaxis_title='Ventas ($)',
        showlegend=True,
        autosize=True
    )
    daily_series_graph_html = daily_series_chart.to_html(full_html=False)

    # Gráfico de Ventas Mensuales
    monthly_series_chart = go.Figure()
    monthly_series_chart.add_trace(
        go.Scatter(
            x=monthly_sales_date,
            y=monthly_sales_values,
            mode='lines+markers',
            name='Ventas Mensuales',
        )
    )
    monthly_series_chart.update_layout(
        title='Ventas Mensuales',
        xaxis_title='Fecha',
        yaxis_title='Ventas ($)',
        showlegend=True,
        autosize=True
    )
    monthly_series_graph_html = monthly_series_chart.to_html(full_html=False)

    # Gráfico de Ventas Trimestrales
    quarterly_series_chart = go.Figure()
    quarterly_series_chart.add_trace(
        go.Scatter(
            x=quarterly_sales_date,
            y=quarterly_sales_values,
            mode='lines+markers',
            name='Ventas Trimestrales',
        )
    )
    quarterly_series_chart.update_layout(
        title='Ventas Trimestrales',
        xaxis_title='Fecha',
        yaxis_title='Ventas ($)',
        showlegend=True,
        autosize=True
    )
    quarterly_series_graph_html = quarterly_series_chart.to_html(full_html=False)

    # Gráfico de Ventas Anuales
    yearly_series_chart = go.Figure()
    yearly_series_chart.add_trace(
        go.Scatter(
            x=yearly_sales_date,
            y=yearly_sales_values,
            mode='lines+markers',
            name='Ventas Anuales',
        )
    )
    yearly_series_chart.update_layout(
        title='Ventas Anuales',
        xaxis_title='Fecha',
        yaxis_title='Ventas ($)',
        showlegend=True,
        autosize=True
    )
    yearly_series_graph_html = yearly_series_chart.to_html(full_html=False)

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
    page_number = request.GET.get('page')
    sales = sales_paginator.get_page(page_number)

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

        'category_graph_html': category_graph_html,
        'subcategory_graph_html': subcategory_graph_html,

        'daily_series_graph_html': daily_series_graph_html,
        'monthly_series_graph_html': monthly_series_graph_html,
        'quarterly_series_graph_html': quarterly_series_graph_html,
        'yearly_series_graph_html': yearly_series_graph_html,

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
