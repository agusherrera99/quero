from django.urls import path

from . import views


app_name = 'summary'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('delete/<int:pk>/', views.delete_sale, name='delete_sale'),
]