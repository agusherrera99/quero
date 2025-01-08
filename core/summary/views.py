from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from pos.models import Sale
from .forms import SalesForm

@login_required
def summary(request):
    # Obtener las ventas del usuario
    sales = Sale.objects.filter(user=request.user).order_by('-created_at')
    
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
        .order_by('-total_quantity')[:10]
    
    # Paginación de los productos más vendidos
    top_sales_paginator = Paginator(top_sales, 10)
    page_number = request.GET.get('page')
    top_sales = top_sales_paginator.get_page(page_number)

    context = {
        'sales': sales,  # ventas paginadas (o resultados de búsqueda paginados)
        'sales_results': sales_results,  # resultados de búsqueda
        'sale_search_form': sale_search_form,  # formulario de búsqueda
        'sale_query': sale_query,  # consulta de búsqueda
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
