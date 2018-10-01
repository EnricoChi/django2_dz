from django.db import models

from commons.models import BaseRankModel


class Company(BaseRankModel):
    class Meta:
        ordering = ('name',)

    REGION = ((0, ''),
              (1, 'Санкт-Петербург'),
              (2, 'Москва'))

    category = models.ForeignKey(
        'CompanyCategory', verbose_name='Category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        'Company name', max_length=128)
    region = models.PositiveSmallIntegerField(
        'Region', choices=REGION, default=0)
    type = models.CharField(
        'Type', max_length=255)
    site = models.CharField(
        'Site', max_length=128)

    price = models.DecimalField(
        'Price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(
        'Quantity', default=0)

    def __str__(self):
        return f'{self.name} - {self.category.name}'

    @staticmethod
    def get_items():
        return Company.objects.filter(is_published=True).order_by('category', 'name')


class CompanyCategory(BaseRankModel):
    name = models.CharField(
        'Category name', max_length=128)

    def __str__(self):
        return self.name
