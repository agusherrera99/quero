# from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration_view, name='register'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('delete-account/submit/', views.delete_account_confirm, name='delete_account_confirm'),
    path('create-sub-account/', views.create_sub_account, name='create_sub_account'),
    path('create-sub-account/submit/', views.add_sub_account, name='add_sub_account'),
    path('delete-sub-account/<int:sub_account_id>/', views.delete_sub_account, name='delete_sub_account'),
    path('support/', views.support, name='support'),
    path('support/submit/', views.receive_support_email, name='receive_support_email'),
    path('select-business-type/', views.business_type_selection, name='business_type_selection'),
    path('select-business-type/submit/', views.select_business_type, name='select_business_type'),
    path('mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]