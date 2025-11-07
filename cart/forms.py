from .models import Order
from django import forms
from django.db import models
class Order_form(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,  # or forms.Select
        label="Select Payment Method"
    )
    class Meta:
            model = Order
            fields=['address','phone','payment_method']