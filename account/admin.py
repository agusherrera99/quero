from django.contrib import admin

from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'shop_name', 'first_name', 'last_name', 'phone', 'tier','is_paid', 'payment_due', 'created_at', 'is_active']
    list_filter = ['is_active', 'is_paid', 'tier']
    search_fields = ['email', 'shop_name', 'first_name', 'last_name']
    prepopulated_fields = {'username': ('first_name', 'last_name', 'shop_name')}
    date_hierarchy = 'created_at'
    show_facets = admin.ShowFacets.ALWAYS