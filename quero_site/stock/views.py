from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from . import forms
from . import models


@login_required
def stock(request):
    return render(request, 'stock/stock.html')

def add_stock(request):
    form = forms.AddProductForm(request.POST or None)
    return render(request, 'stock/add_stock.html', {'form': form})

def edit_stock(request, pk):
    return render(request, 'stock/edit_stock.html')

def delete_stock(request, pk):
    return render(request, 'stock/delete_stock.html')


def load_subcategories(request):
    category_id = request.Get.get('category_id')
    subcategories = models.Subcategory.objects.filter(category_id=category_id).all()
    return JsonResponse({'subcategories': list(subcategories.values('id', 'name'))})