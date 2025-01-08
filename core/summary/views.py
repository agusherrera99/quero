from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pos.models import Sale

@login_required
def summary(request):
    # Obtener las ventas del usuario
    sales = Sale.objects.filter(user=request.user).order_by('-created_at')
    print(sales)
    context = {
        'sales': sales,
    }

    return render(request, 'summary/summary.html', context)
