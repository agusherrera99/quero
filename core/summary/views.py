from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def summary(request):
    return render(request, 'summary/summary.html')
