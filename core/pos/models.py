from django.db import models
from django.forms import ValidationError



class Sale(models.Model):
    product = models.ForeignKey('stock.Product', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'sales'

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('La cantidad no puede ser negativa')

    def __str__(self):
        return self.product.name + ' - ' + str(self.quantity) + ' - ' + str(self.created_at)