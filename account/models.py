from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class BusinessType(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin tipo')
    description = models.TextField(null=True, blank=True)
    category_list = models.ManyToManyField('stock.Category', related_name='business_types')

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='business_type_name_idx'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.description = self.description.lower()
        return super(BusinessType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class TierModel(models.Model):
    name = models.CharField(max_length=50, null=False, default='gratuito')
    duration = models.IntegerField(default=15)

def get_default_payment_due_date():
    return timezone.localtime(timezone.now()) + timezone.timedelta(days=15)

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=30, default='0')
    shop_name = models.CharField(max_length=100, default='sin nombre')
    address = models.CharField(max_length=255, null=True, blank=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True, blank=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    tier = models.ForeignKey(TierModel, on_delete=models.CASCADE, null=True, blank=True, default=1)
    payment_due = models.DateTimeField(null=True, default=get_default_payment_due_date)
    is_sub_account = models.BooleanField(default=False)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['shop_name'], name='shop_name_idx'),
        ]

    def save(self, *args, **kwargs):
        # Extraer un parámetro para indicar si es un superusuario desde manage.py
        is_superuser_from_command = kwargs.pop('skip_lower', False)
        
        # Aplicar transformaciones a minúsculas solo si no es un superusuario desde comando
        if not is_superuser_from_command:
            if self.shop_name:
                self.shop_name = self.shop_name.lower()
            if self.address:
                self.address = self.address.lower()
        
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())  
        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.username}"
        
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    # Marcar la notificación como leída
    def mark_as_read(self):
        self.is_read = True
        self.delete()