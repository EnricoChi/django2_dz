from django.db import models
from django.conf import settings
from rank_item.models import Company
from commons.models import BaseRankModel


class Basket(BaseRankModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, verbose_name='Company', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity', default=0)

    def _get_product_cost(self):
        return self.company.price * self.quantity

    product_cost = property(_get_product_cost)

    def _get_total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    total_cost = property(_get_total_cost)

    @staticmethod
    def get_items(user):
        return user.basket_set.all()
