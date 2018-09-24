from django import forms

from commons.forms import BaseForm
from .models import Order, OrderItem


class OrderForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(BaseForm, forms.ModelForm):
    price = forms.CharField(
        label='Price', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'
