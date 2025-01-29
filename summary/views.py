from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, IntegerField, Sum, Value, When
from django.db.models.functions import TruncDate, TruncMonth, TruncQuarter, TruncYear
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
    
def get_sales_data_for_period(sales, period):
    # Definir las fechas de inicio y fin basadas en el período
    today = datetime.today()
    start_date = today - timedelta(days=period)

    # Agrupar las ventas por diferentes periodos de tiempo (día, mes, trimestre, año)
    sales_by_day = sales.filter(created_at__gte=start_date).annotate(day=TruncDate('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    sales_by_month = sales.filter(created_at__gte=start_date).annotate(month=TruncMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by('month')
    sales_by_quarter = sales.filter(created_at__gte=start_date).annotate(quarter=TruncQuarter('created_at')).values('quarter').annotate(total_sales=Sum('total_price')).order_by('quarter')
    sales_by_year = sales.filter(created_at__gte=start_date).annotate(year=TruncYear('created_at')).values('year').annotate(total_sales=Sum('total_price')).order_by('year')

    # Extraer las fechas y los valores de ventas de cada período
    def extract_sales_data(sales_data):
        if sales_data:
            sales_date = [sale['day'] if 'day' in sale else sale['month'] if 'month' in sale else sale['quarter'] if 'quarter' in sale else sale['year'] for sale in sales_data]
            sales_values = [sale['total_sales'] for sale in sales_data]
            return sales_date, sales_values
        return [], []

    # Extraer los datos de ventas por período
    daily_sales_date, daily_sales_values = extract_sales_data(sales_by_day)
    monthly_sales_date, monthly_sales_values = extract_sales_data(sales_by_month)
    quarterly_sales_date, quarterly_sales_values = extract_sales_data(sales_by_quarter)
    yearly_sales_date, yearly_sales_values = extract_sales_data(sales_by_year)

    return (daily_sales_date, daily_sales_values, monthly_sales_date, monthly_sales_values, quarterly_sales_date, quarterly_sales_values, yearly_sales_date, yearly_sales_values)

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
    
    # Ventas por Categoría y Subcategoría
    category_and_subcategory_sales = Sale.objects.values(
        'product__subcategory__category__name',
        'product__subcategory__name'
    ).annotate(
        total_sales=Sum('total_price')
    ).filter(user=request.user).order_by('-total_sales')

    # Gráfico de Ventas por Categoría (Pie Chart)
    # Ventas totales por Categoría
    category_sales_labels = [sale['product__subcategory__category__name'] for sale in category_and_subcategory_sales]
    category_sales_values = [sale['total_sales'] for sale in category_and_subcategory_sales]

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
    subcategory_sales_labels = [sale['product__subcategory__name'] for sale in category_and_subcategory_sales]
    subcategory_sales_values = [sale['total_sales'] for sale in category_and_subcategory_sales]

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
    daily_sales_date, daily_sales_values, monthly_sales_date, monthly_sales_values, quarterly_sales_date, quarterly_sales_values, yearly_sales_date, yearly_sales_values = get_sales_data_for_period(sales, 365)

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
