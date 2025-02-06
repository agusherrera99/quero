from django.db import models


class SpendCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Spend(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(SpendCategory, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.created_at} - {self.category} - {self.amount} - {self.receiver}'
    
    class Meta:
        ordering = ['-created_at']
        