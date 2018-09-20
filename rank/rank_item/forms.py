from django import forms

from commons.forms import BaseForm
from rank_item.models import Company, CompanyCategory


class CompanyForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'site', 'region', 'type', 'category', 'price', 'quantity', 'is_published')


class CompanyCategoryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = CompanyCategory
        fields = ('name', 'is_published')
