from django.urls import path

from . import views


app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('pages/select-business-type/', views.business_type_selection, name='business_type_selection'),
    path('pages/select-business-type/submit/', views.select_business_type, name='select_business_type'),
]