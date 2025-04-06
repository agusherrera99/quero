from django.contrib import admin

# Register your models here.

from .models import Category, Subcategory, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 10
    list_editable = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )
    readonly_fields = ('id',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    ordering = ('name',)
    list_per_page = 10
    list_editable = ('name', 'category')
    fieldsets = (
        (None, {
            'fields': ('name', 'category')
        }),
    )
    readonly_fields = ('id',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price', 'cost', 'barcode', 'uom', 'subcategory')
    search_fields = ('name', 'barcode')
    list_filter = ('subcategory',)
    ordering = ('name',)
    list_per_page = 10
    list_editable = ('name', 'quantity', 'price', 'cost', 'barcode', 'uom', 'subcategory')
    fieldsets = (
        (None, {
            'fields': ('name', 'quantity', 'price', 'cost', 'barcode', 'uom', 'subcategory')
        }),
    )
    readonly_fields = ('id',)