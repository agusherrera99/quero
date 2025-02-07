from django import forms

from . import models

class SpendForm(forms.Form):
    spend_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buscar gasto'
            }
        )
    )

class AddSpendForm(forms.ModelForm):
    class Meta:
        model = models.Spend
        fields = ('category', 'amount', 'receiver')

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

    category = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        required=True,
        help_text='Seleccione la categoría del gasto.',
        label='Categoría',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    amount = forms.DecimalField(
        required=True,
        help_text='Proporcione el monto del gasto.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Monto del gasto'
            }
        )
    )

    receiver = forms.CharField(
        max_length=100,
        required=True,
        help_text='Proporcione el receptor del gasto.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Receptor del gasto'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddSpendForm, self).__init__(*args, **kwargs)