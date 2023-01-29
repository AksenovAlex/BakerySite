from .models import *

from django import forms

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name',
            'phone',
            'address',
            'comment',
        )