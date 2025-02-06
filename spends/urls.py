from django.urls import path

from . import views

app_name = 'spends'

urlpatterns = [
    path('', views.spends, name='spends'),
    path('spends-data/', views.spends_data, name='spends_data'),
    path('category-spends-data/', views.category_spends_data, name='category_spends_data'),
]