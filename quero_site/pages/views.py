from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import scipts


def home(request):
    return render(request, 'home.html')

@login_required
def business_type_selection(request):
    business_types = scipts.generate_business_types()
    return render(request, 'pages/business_type_selection.html', {'business_types': business_types})

@login_required
def select_business_type(request):
    if request.method == 'POST':
        business_type = request.POST.get('business_type')
        
        request.user.profile.business_type = business_type
        request.user.profile.save()
        return redirect('accounts:profile')
    return render('pages/business_type_selection')