from django.db import models


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