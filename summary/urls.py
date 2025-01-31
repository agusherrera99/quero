from django.urls import path

from . import views


app_name = 'summary'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('sales-data/', views.sales_data, name='sales_data'),
    path('category-sales-data/', views.category_sales_data, name='category_sales_data'),
    path('subcategory-sales-data/', views.subcategory_sales_data, name='subcategory_sales_data'),
    path('delete/<int:pk>/', views.delete_sale, name='delete_sale'),
]