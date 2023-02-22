from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *

from django import forms


class OrderForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес'}), required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Комментарий к заказу'}))

    class Meta:
        model = Order
        fields = (
            'first_name',
            'phone',
            'address',
            'comment',
        )


class LoginClientForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    password = forms.Field(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class RegistrationForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['address'].label = 'Адрес'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято. Попробуйте другое.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'phone', 'address', 'password', 'confirm_password']
