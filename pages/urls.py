from django.urls import path

from . import views


app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('prices/', views.prices, name='prices'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.receive_contact_email, name='receive_contact_email'),
    path('select-business-type/', views.business_type_selection, name='business_type_selection'),
    path('select-business-type/submit/', views.select_business_type, name='select_business_type'),
]