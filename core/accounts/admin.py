from django.contrib import admin

from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'shop_name', 'first_name', 'last_name', 'phone', 'updated_at', 'created_at', 'is_active', 'is_paid', 'payment_due']
    list_filter = ['created_at', 'updated_at', 'is_active']
    search_fields = ['email', 'shop_name', 'first_name', 'last_name']
    prepopulated_fields = {'username': ('first_name', 'last_name', 'shop_name')}
    date_hierarchy = 'updated_at'
    show_facets = admin.ShowFacets.ALWAYS