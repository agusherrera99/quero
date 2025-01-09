from django.db import models
from django.forms import ValidationError
from django.utils import timezone


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin subcategoria')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'subcategories'
        indexes = [
            models.Index(fields=['name'], name='subcategory_name_idx'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin categoria')

    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['name'], name='category_name_idx'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    UNIT_CHOICES = [
        ('unidad', 'Unidad'),
        ('kilogramo', 'Kilogramo'),
        ('miligramo', 'Miligramo'),
        ('mililitros', 'Mililitros'),
    ]

    name = models.CharField(max_length=100, null=False, default='sin nombre')
    quantity = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0)
    uom = models.CharField(max_length=30, choices=UNIT_CHOICES, null=False, default='unidad')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['name'], name='product_name_idx'),
            models.Index(fields=['quantity'], name='product_quantity_idx'),
            models.Index(fields=['price'], name='product_price_idx'),
            models.Index(fields=['uom'], name='product_uom_idx'),
            models.Index(fields=['created_at'], name='product_created_at_idx'),
            models.Index(fields=['updated_at'], name='product_updated_at_idx'),
        ]

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.uom = self.uom.lower()

        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())  

        if self.updated_at is None:
            self.updated_at = timezone.localtime(timezone.now())  

        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

        if self.quantity < 0:
            raise ValidationError('La cantidad no puede ser negativa')

        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name