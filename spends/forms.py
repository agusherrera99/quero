from django import forms

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