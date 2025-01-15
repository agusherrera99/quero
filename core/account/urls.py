# from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration_view, name='register'),
    path('marcar-leida/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]