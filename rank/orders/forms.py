from django import forms

from commons.forms import BaseForm
from rank_item.models import Company
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.get_items().select_related()
