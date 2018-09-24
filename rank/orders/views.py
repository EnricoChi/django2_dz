from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from django.urls import reverse_lazy

from basket.models import Basket

from .models import Order, OrderItem
from .forms import OrderItemForm


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        parent = super().get_queryset()
        return parent.filter(user=self.request.user)


class OrderItemAdd(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1)

        basket = Basket.get_items(self.request.user)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
            basket.delete()
        else:
            if len(basket):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket))
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['company'] = basket[num].company
                    form.initial['quantity'] = basket[num].quantity
                    form.initial['price'] = basket[num].company.price

            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderItemEdit(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1)

        formset = OrderFormSet(self.request.POST or None, instance=self.object)

        for form in formset.forms:
            if form.instance.pk:
                form.initial['price'] = form.instance.company.price

        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


def order_del(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('orders:orders-all')


class OrderView(DetailView):
    model = Order
