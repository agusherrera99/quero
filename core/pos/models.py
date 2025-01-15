from decimal import Decimal, ROUND_DOWN

from django.db import models
from django.forms import ValidationError



class Sale(models.Model):
    product = models.ForeignKey('stock.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'sales'
        indexes = [
            models.Index(fields=['created_at'], name='sale_created_at_idx'),
        ]

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        
        if self.total_price < 0:
            raise ValidationError('El precio total no puede ser negativo')
        
    def save(self, *args, **kwargs):
        self.total_price = self.total_price.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        self.full_clean()  # This will call the clean method and validate the instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.created_at}] {self.product.name} x {self.quantity} - Total: ${self.total_price}'
