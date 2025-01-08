from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.shortcuts import render

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

    context = {
        'sales': sales,  # ventas paginadas (o resultados de búsqueda paginados)
        'sales_results': sales_results,  # resultados de búsqueda
        'sale_search_form': sale_search_form,  # formulario de búsqueda
        'sale_query': sale_query,  # consulta de búsqueda
    }

    return render(request, 'summary/summary.html', context)
