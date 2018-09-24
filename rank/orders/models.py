from django.db import models
from django.conf import settings

from rank_item.models import Company
from commons.models import BaseRankModel


class Order(BaseRankModel):
    ORDER_STATUS_CHOICES = (
        (0, 'waiting'),
        (1, 'approved'),
        (2, 'completed'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        'Status', choices=ORDER_STATUS_CHOICES, default=0)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.order_items.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity * x.company.price, items)))

    def delete(self, *args, **kwargs):
        for item in self.order_items.select_related():
            item.company.quantity += item.quantity
            item.company.save()
        super().delete()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_items', on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, verbose_name='Company', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity', default=0)

    def get_product_cost(self):
        return self.company.price * self.quantity

    def delete(self, *args, **kwargs):
        self.company.quantity += self.quantity
        self.company.save()
        super().delete()

    def save(self, *args, **kwargs):
        if self.pk:
            self.company.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.company.quantity -= self.quantity
        self.company.save()
        super().save(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()
