from django.db import models
from django.utils import timezone


class Spend(models.Model):
    CATEGORIES_CHOICES = [
        ('alquiler', 'Alquiler'),
        ('electricidad', 'Electricidad'),
        ('agua', 'Agua'),
        ('internet', 'Internet'),
        ('las', 'Gas'),
        ('teléfono', 'Teléfono'),
        ('insumos y materias primas', 'Insumos y Materias Primas'),
        ('sueldos', 'Sueldos'),
        ('bonificaciones', 'Bonificaciones'),
        ('seguridad social', 'Seguridad Social'),
        ('combustible', 'Combustible'),
        ('mantenimiento', 'Mantenimiento'),
        ('reparaciones', 'Reparaciones'),
        ('impuestos', 'Impuestos'),
        ('seguros', 'Seguros'),
        ('prestamos y financiamientos', 'Préstamos y Financiamientos'),
        ('gastos inesperados', 'Gastos Inesperados'),
        ('inversión en infraestructura', 'Inversión en Infraestructura'),
    ]

    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORIES_CHOICES)
    receiver = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.created_at} - {self.category} - {self.amount} - {self.receiver}'
    
    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())  

        if self.amount < 0:
            raise ValueError('El monto no puede ser negativo')

        return super(Spend, self).save(*args, **kwargs)