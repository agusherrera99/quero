from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=30, default='0')
    shop_name = models.CharField(max_length=100, default='sin nombre')
    business_type = models.ForeignKey('pages.BusinessType', on_delete=models.CASCADE, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.shop_name = self.shop_name.lower()
        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.username}"