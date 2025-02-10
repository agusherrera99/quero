from django.urls import path

from . import views


app_name = 'stock'

urlpatterns = [
    path('', views.stock, name='stock'),
    path('download/', views.download_stock, name='download_stock'),
    path('download-csv-template/', views.download_csv_template, name='download_csv_template'),
    path('import/', views.import_stock, name='import_stock'),
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),
    path('add/', views.add_stock, name='add_stock'),
    path('edit/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('delete/<int:pk>/', views.delete_stock, name='delete_stock'),
]