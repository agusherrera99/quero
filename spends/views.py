from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, IntegerField, F, Sum, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from spends.models import Spend
from spends.forms import AddSpendForm, SpendForm


def thousand_separator(value):
    if value is None:
        return "0.0"
    return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")

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
    
def get_spend_data_for_period(user, period):
    today = datetime.today()
    start_date = today - timedelta(days=period)

    # Usar una consulta agregada con `values` y `annotate` más eficiente
    spend_data = Spend.objects.filter(user=user, created_at__date__gte=start_date).values(
        'created_at__date'
    ).annotate(
        amount=Sum('amount')
    ).order_by('created_at__date')

    spends_dates = [entry['created_at__date'].strftime('%Y-%m-%d') for entry in spend_data]
    spends_values = [entry['amount'] for entry in spend_data]

    result = {'dates': spends_dates, 'values': spends_values}
    return result

@login_required
def spends_data(request):
    period = request.GET.get('period', 7)
    period = int(period[:-1])

    if request.user.is_sub_account:
        data = get_spend_data_for_period(request.user.parent_account.id, period)
    else:
        data = get_spend_data_for_period(request.user, period)

    return JsonResponse(data)

def get_category_spends_data(user):
    category_spends = Spend.objects.filter(user=user).values(
        category_name=F('category')
    ).annotate(
        total_spends=Sum('amount')
    ).order_by('-total_spends')

    category_labels = [entry['category_name'] for entry in category_spends]
    category_values = [entry['total_spends'] for entry in category_spends]

    result = {'labels': category_labels, 'values': category_values}
    return result

@login_required
def category_spends_data(request):
    if request.user.is_sub_account:
        data = get_category_spends_data(request.user.parent_account.id)
    else:
        data = get_category_spends_data(request.user)
    return JsonResponse(data)

@login_required
def spends(request):
    # Obtener los gastos del usuario
    if request.user.is_sub_account:
        spends = Spend.objects.filter(user=request.user.parent_account.id).order_by('-created_at')
    else:
        spends = Spend.objects.filter(user=request.user).order_by('-created_at')

    # Calcular el primer dia del més actual y el día anterior
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    yesterday = today - timedelta(days=1)
    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

    # Gastos de hoy y ayer
    daily_spends_data = spends.aggregate(
        total_spends_today=Sum(Case(
            When(created_at__date=today, then=F('amount')),
            default=Value(0),
            output_field=IntegerField()
        )),
        total_spends_yesterday=Sum(Case(
            When(created_at__date=yesterday, then=F('amount')),
            default=Value(0),
            output_field=IntegerField()
        ))
    )
    daily_spends = daily_spends_data.get('total_spends_today', 0) if daily_spends_data else 0
    daily_spends_yesterday = daily_spends_data.get('total_spends_yesterday', 0) if daily_spends_data else 0
    daily_spends_percentage, daily_spends_percentage_text, daily_spends_percentage_color = calculate_percentage_change(daily_spends, daily_spends_yesterday)

    daily_spends = thousand_separator(daily_spends)

    # Gastos del mes actual y del mes pasado
    monthly_spends_data = spends.filter(created_at__date__gte=first_day_current_month).aggregate(
        total_spends=Sum('amount')
    )
    monthly_spends = monthly_spends_data.get('total_spends', 0) if monthly_spends_data else 0
    monthly_spends_last_month_data = spends.filter(created_at__date__gte=first_day_last_month, created_at__date__lt=first_day_current_month).aggregate(
        total_spends=Sum('amount')
    )
    monthly_spends_last_month = monthly_spends_last_month_data.get('total_spends', 0) if monthly_spends_last_month_data else 0
    monthly_spends_percentage, monthly_spends_percentage_text, monthly_spends_percentage_color = calculate_percentage_change(monthly_spends, monthly_spends_last_month)

    monthly_spends = thousand_separator(monthly_spends)

    # Buscador de ventas
    spend_search_form = SpendForm()
    spend_query = None
    spends_results = []

    if 'spend_query' in request.GET:
        spend_search_form = SpendForm(request.GET)
        if spend_search_form.is_valid():
            spend_query = spend_search_form.cleaned_data['spend_query']
            spends_results = spends.annotate(
            search=SearchVector('category')
        ).filter(search__icontains=spend_query)

    spends_paginator = Paginator(spends_results if spends_results else spends, 10)
    page_number = request.GET.get('page', 1)
    spends = spends_paginator.get_page(page_number)

    context = {
        'daily_spends': daily_spends,
        'daily_spends_percentage': daily_spends_percentage,
        'daily_spends_percentage_text': daily_spends_percentage_text,
        'daily_spends_percentage_color': daily_spends_percentage_color,

        'monthly_spends': monthly_spends,
        'monthly_spends_percentage': monthly_spends_percentage,
        'monthly_spends_percentage_text': monthly_spends_percentage_text,
        'monthly_spends_percentage_color': monthly_spends_percentage_color,

        'spends': spends,
        'results': spends_results,
        'spend_search_form': spend_search_form,
        'spend_query': spend_query
    }

    return render(request, 'spends.html', context=context)

@login_required
@transaction.atomic
def add_spend(request):
    if request.method == 'POST':
        form = AddSpendForm(request.POST)
        if form.is_valid():
            action = request.POST.get('action')

            if action == 'add_and_finish':

                category = form.cleaned_data.get('category')
                amount = form.cleaned_data.get('amount')
                receiver = form.cleaned_data.get('receiver')

                spend = Spend(
                    user=request.user,
                    category=category,
                    amount=amount,
                    receiver=receiver
                )
                spend.save()
                messages.success(request, 'Gasto añadido correctamente.')
                return redirect('spends:spends')
            elif action == 'add_and_continue':
                category = form.cleaned_data.get('category')
                amount = form.cleaned_data.get('amount')
                receiver = form.cleaned_data.get('receiver')

                spend = Spend(
                    user=request.user,
                    category=category,
                    amount=amount,
                    receiver=receiver
                )
                spend.save()
                messages.success(request, 'Gasto añadido correctamente.')
                return redirect('spends:add_spend')
        else:
            messages.error(request, 'Ocurrió un error al añadir el gasto.')
    else:
        form = AddSpendForm()

    context = {
        'form': form
    }

    return render(request, 'add_spend.html', context)

@login_required
@transaction.atomic
def edit_spend(request, pk):
    spend = Spend.objects.filter(pk=pk).first()

    if request.user.is_sub_account:
        if spend.user != request.user.parent_account:
            messages.error(request, 'No tienes permisos para editar este gasto.')
            return redirect('spends:spends')
    else:
        if spend.user != request.user:
            messages.error(request, 'No tienes permisos para editar este gasto.')
            return redirect('spends:spends')

    if request.method == 'POST':
        form = AddSpendForm(data=request.POST, instance=spend, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto editado correctamente.')
            return redirect('spends:spends')
        else:
            messages.error(request, 'Ocurrió un error al editar el gasto.')
    else:
        form = AddSpendForm(instance=spend, request=request)

    context = {
        'form': form
    }

    return render(request, 'edit_spend.html', context)

@login_required
@transaction.atomic
def delete_spend(request, pk):
    spend = get_object_or_404(Spend, pk=pk)

    if request.user.is_sub_account:
        if spend.user != request.user.parent_account:
            messages.error(request, 'No tienes permisos para eliminar este gasto.')
            return redirect('spends:spends')
    else:
        if spend.user != request.user:
            messages.error(request, 'No tienes permisos para eliminar este gasto.')
            return redirect('spends:spends')
    
    if request.method == 'POST':
        spend.delete()
        messages.success(request, 'Gasto eliminado correctamente.')
        return redirect('spends:spends')

    context = {
        'spend': spend
    }
    return render(request, 'delete_spend.html', context)