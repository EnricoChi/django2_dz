from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderList.as_view(), name='orders-all'),
    path('view/', views.OrderView.as_view(), name='order-view'),
    path('add/', views.OrderItemAdd.as_view(), name='order-add'),
    path('edit/<int:pk>', views.OrderItemEdit.as_view(), name='order-edit'),
    path('delete/<int:pk>', views.order_del, name='order-del'),
    # re_path(r'^forming/complete/(?P<pk>\d+)/$',
    #    ordersapp.order_forming_complete, name='order_forming_complete'),
]
