from django import forms

class SalesForm(forms.Form):
    sale_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buscar venta'
            }
        )
    )