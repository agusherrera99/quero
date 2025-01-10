from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=30, default='0')
    shop_name = models.CharField(max_length=100, default='sin nombre')
    business_type = models.ForeignKey('pages.BusinessType', on_delete=models.CASCADE, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    payment_due = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['shop_name'], name='shop_name_idx'),
        ]

    def save(self, *args, **kwargs):
        self.shop_name = self.shop_name.lower()
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())  
        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.username}"