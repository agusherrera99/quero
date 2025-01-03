from django import forms

from . import models


class AddProductForm(forms.Form):
    model = models.Product
    fields = ('name', 'quantity', 'price', 'uom', 'subcategory')

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

    uom = forms.CharField(
        max_length=30,
        required=False,
        help_text='Proporcione la unidad de medida del producto.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Unidad de medida'
            }
        )
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = self.data.get('category')
                self.fields['subcategory'].queryset = models.Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass