from django.db import models
from .managers import OrderManager


class OrderCustomer(models.Model):
    customer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Order(models.Model):
    """订单"""

    # 订单状态
    ORDER_STATUS = (
        (1, 'Received'),
        (2, 'Processing'),
        (3, 'Payment complete'),
        (4, 'Shipping'),
        (5, 'Completed'),
        (6, 'Cancelled'),
    )

    # 订单客户
    order_customer = models.ForeignKey(
        OrderCustomer,
        on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=ORDER_STATUS, default='1')

    objects = OrderManager()


class OrderItems(models.Model):
    """订单项"""
    class Meta:
        verbose_name_plural = 'Order items'

    product_id = models.IntegerField()
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    # 单位价格
    price_per_unit = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )
    # 订单
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
