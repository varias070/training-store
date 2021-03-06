from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import ReviewProduct


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]
PRODUCT_REVIEW_CHOICES = [(i, str(i)) for i in range(1, 5)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ChangePersonalInformationForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'autofocus': True, 'class': 'form-control'}),
    )


class ReviewProductForm(forms.ModelForm):
    user = forms.EmailField(label='Пользователь', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    review = forms.TypedChoiceField(label='Оценка', choices=PRODUCT_REVIEW_CHOICES, coerce=int, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ReviewProduct
        fields = ('user', 'review', 'description')
