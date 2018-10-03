from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.conf import settings
from django.core.cache import cache

from .models import Company


class CompanyView(DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category
        # context['category_items'] = Company.objects.filter(is_published=True, category=category).order_by('name')
        context['category_items'] = get_company_in_category(category)
        return context


def get_company_in_category(category):
    if settings.LOW_CACHE:
        key = f'companies_category_{category.pk}'
        companies = cache.get(key)
        if companies is None:
            companies = Company.objects.filter(is_published=True, category=category).order_by('price')
            cache.set(key, companies)
        return companies
    else:
        return Company.objects.filter(is_published=True, category=category).order_by('price')
