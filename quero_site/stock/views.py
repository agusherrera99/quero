from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from . import forms
from . import models


@login_required
def stock(request):
    products = models.Product.objects.filter(user=request.user).all().order_by('-created_at')
    return render(request, 'stock/stock.html', {'products': products})

@login_required
def add_stock(request):
    if request.method == 'POST':
        form = forms.AddProductForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            quantity = form.cleaned_data.get('quantity')
            price = form.cleaned_data.get('price')
            uom = form.cleaned_data.get('uom')
            subcategory = form.cleaned_data.get('subcategory')

            product = models.Product(
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
        else:
            print(form.errors)
            messages.error(request, 'Formulario no válido. Revisa los campos.')
    else:
        form = forms.AddProductForm()
    
    return render(request, 'stock/add_stock.html', {'form': form})

def edit_stock(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    print(product.subcategory.category)

    if product.user != request.user:
        messages.error(request, 'No tienes permisos para editar este producto.')
        return redirect('stock:stock')

    if request.method == 'POST':
        form = forms.AddProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Producto actualizado correctamente.')
            return redirect('stock:stock')
        else:
            messages.error(request, 'Formulario no válido. Revisa los campos.')
    else:
        form = forms.AddProductForm(instance=product)

    return render(request, 'stock/edit_stock.html', {'form': form})


def delete_stock(request, pk):
    product = get_object_or_404(models.Product, pk=pk)

    if product.user != request.user:
        messages.error(request, 'No tienes permisos para eliminar este producto.')
        return redirect('stock:stock')
    
    if request.method == 'POST':
        product.delete()
        messages.info(request, 'Producto eliminado correctamente.')
        return redirect('stock:stock')

    return render(request, 'stock/delete_stock.html', {'product': product})

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = models.Subcategory.objects.filter(category_id=category_id).order_by('name')

    # Creamos un diccionario con las subcategorías que vamos a devolver
    subcategory_data = [{"id": subcategory.id, "name": subcategory.name} for subcategory in subcategories]
    return JsonResponse({"subcategories": subcategory_data})