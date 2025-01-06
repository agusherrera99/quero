from decimal import Decimal, InvalidOperation
from django import forms

from . import models


class AddProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ('name', 'quantity', 'price', 'uom', 'subcategory')

    UNIT_CHOICES = [
        ('unidad', 'Unidad'),
        ('kilogramo', 'Kilogramo'),
        ('miligramo', 'Miligramo'),
        ('mililitros', 'Mililitros'),
    ]

    name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Proporcione un nombre para el producto.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }
        )
    )

    quantity = forms.IntegerField(
        required=True,
        help_text='Proporcione la cantidad disponible del producto.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible'
            }
        )
    )

    price = forms.DecimalField(
        required=True,
        help_text='Proporcione el precio del producto.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Precio del producto'
            }
        )
    )

    uom = forms.ChoiceField(
        choices=UNIT_CHOICES,  # Usa las opciones predefinidas
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Unidad de Medida'
    )

    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(),
        required=True,
        help_text='Seleccione una categoría para el producto.',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Categoría'
    )

    subcategory = forms.ModelChoiceField(
        queryset=models.Subcategory.objects.none(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Subcategoría'
    )

    def clean_price(self):
        price = self.cleaned_data['price']
        try:
            price = Decimal(price)
        except InvalidOperation:
            raise forms.ValidationError("El precio debe ser un número válido.")
        
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si existe un valor para 'category' en los datos del formulario (ya sea al editar o al ser enviado)
        if 'category' in self.data:
            try:
                # Obtén la categoría seleccionada
                category_id = self.data.get('category')
                # Actualiza las subcategorías disponibles según la categoría seleccionada
                self.fields['subcategory'].queryset = models.Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            category_id = self.instance.subcategory.category.id
            # Si se está editando un producto, establecer el queryset de las subcategorías según la categoría actual
            self.fields['subcategory'].queryset = models.Subcategory.objects.filter(category_id=category_id).order_by('name')
            # Fuerza la preselección de la categoría si no se está seleccionando correctamente
            self.fields['category'].initial = self.instance.subcategory.category