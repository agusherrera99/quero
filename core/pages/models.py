from django.db import models

from accounts.models import CustomUser


class BusinessType(models.Model):
    name = models.CharField(max_length=100, null=False, default='sin tipo')
    description = models.TextField(null=True, blank=True)
    category_list = models.ManyToManyField('stock.Category', related_name='business_types', default=1)

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
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message