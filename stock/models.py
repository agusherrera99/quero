from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from account.models import Notification

class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin subcategoria', verbose_name='Subcategoría')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1, verbose_name='Categoría')

    class Meta:
        db_table = 'subcategories'
        indexes = [
            models.Index(fields=['name'], name='subcategory_name_idx'),
        ]
        verbose_name = 'Subcategoría'
        verbose_name_plural = 'Subcategorías'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin categoria', verbose_name='Categoría')

    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['name'], name='category_name_idx'),
        ]
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    UNIT_CHOICES = [
        ('unidad', 'Unidad'),
        ('kilogramo', 'Kilogramo'),
        ('gramo', 'Gramo'),
        ('litro', 'Litro'),
        ('mililitro', 'Mililitro'),
    ]

    LOW_THRESHOLD = 5

    name = models.CharField(max_length=100, null=False, default='sin nombre', verbose_name='Nombre')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0, verbose_name='Cantidad')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0, verbose_name='Precio')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0, verbose_name='Costo')
    barcode = models.CharField(max_length=100, null=True, default=None, verbose_name='Código de barras')
    uom = models.CharField(max_length=30, choices=UNIT_CHOICES, null=False, default='unidad', verbose_name='Unidad de medida')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, default=1, verbose_name='Subcategoría')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, null=True)

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
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def is_low_stock(self):
        if self.quantity <= self.LOW_THRESHOLD:
            plural_uom = ""
            if self.uom == "unidad":
                plural_uom = "unidades"
            elif self.uom == "kilogramo":
                plural_uom = "kilogramos"
            elif self.uom == "gramo":
                plural_uom = "gramos"
            elif self.uom == "litro":
                plural_uom = "litros"
            elif self.uom == "mililitro":
                plural_uom = "mililitros"

            Notification.objects.create(
                user=self.user,
                message=f'Stock bajo de {self.name} ({self.quantity} {plural_uom})'
            )

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')
        if self.cost < 0:
            raise ValidationError('El costo no puede ser negativo')

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
        
        if self.cost < 0:
            raise ValidationError('El costo no puede ser negativo')

        # Verificar si el producto está en stock bajo
        self.is_low_stock()

        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name