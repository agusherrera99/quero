from django.db import models


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin subcategoria')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'subcategories'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin categoria')
    business = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'categories'

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

    def __str__(self):
        return self.name