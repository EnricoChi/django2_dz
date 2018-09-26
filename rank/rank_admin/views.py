from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from rank_item.models import Company, CompanyCategory
from rank_item.forms import CompanyForm, CompanyCategoryForm


def admin_main(request):
    return render(request, 'rank_admin/index.html')


class CompanyAll(ListView):
    model = Company


class CompanyAdd(CreateView):
    model = Company
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('r_admin:company-edit', kwargs={'pk': self.object.pk})


class CompanyEdit(UpdateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('r_admin:company-all')


def company_del(request, pk=None):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return redirect('rank_admin:company-all')


class CompanyCategoryAll(ListView):
    model = CompanyCategory


class CompanyCategoryAdd(CreateView):
    model = CompanyCategory
    form_class = CompanyCategoryForm

    def get_success_url(self):
        return reverse('r_admin:category-edit', kwargs={'pk': self.object.pk})


class CompanyCategoryEdit(UpdateView):
    model = CompanyCategory
    form_class = CompanyCategoryForm
    success_url = reverse_lazy('r_admin:category-all')


def company_category_del(request, pk=None):
    category = get_object_or_404(CompanyCategory, pk=pk)
    category.delete()
    return redirect('rank_admin:category-all')