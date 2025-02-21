from django import forms
from django.contrib.auth import get_user_model


class UserLoginForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone')

    username = forms.CharField(
        max_length=30,
        required=False,
        help_text='Proporcione un nombre de usuario.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'usuario123'
            }
        )
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Proporcione una dirección de correo electrónico válida.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'tucorreo@email.com'
            }
        )
    )

    password = forms.CharField(
        max_length=30,
        required=True,
        help_text='Proporcione una contraseña.',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**********',
                'id': 'password-input'
            }
        )
    )

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'shop_name', 'first_name', 'last_name', 'phone', 'address')

    username = forms.CharField(
        max_length=30,
        required=False,
        help_text='Proporcione un nombre de usuario.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'usuario123'
            }
        )
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Proporcione una dirección de correo electrónico válida.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'tucorreo@email.com'
            }
        )
    )

    password1 = forms.CharField(
        max_length=30,
        required=True,
        help_text='Proporcione una contraseña.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**********'
            }
        )
    )
    
    password2 = forms.CharField(
        max_length=30,
        required=True,
        help_text='Confirme la contraseña.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**********',
            }
        )
    )

    shop_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Proporcione el nombre de su tienda.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mi Tienda'
            }
        )
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Proporcione su nombre.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Juan'
            }
        )
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Proporcione su apellido.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Pérez'
            }
        )
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        help_text='Proporcione su número de teléfono.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1234567890'
            }
        )
    )

    address = forms.CharField(
        max_length=255,
        required=False,
        help_text='Proporcione su dirección.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Calle 123'
            }
        )
    )