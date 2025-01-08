from django.urls import path

from . import views


app_name = 'pos'

urlpatterns = [
    path('', views.pos, name='pos'),
    path('confirm/', views.sales_confirmation, name='sales_confirmation'),
    path('confirm/process/', views.process_sale, name='process_sale'),
    path('cancel/', views.cancel_sale, name='cancel_sale'),
]