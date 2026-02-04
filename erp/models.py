from django.db import models


class SalesOrder(models.Model):
    order_no = models.CharField("订单号", max_length=50, unique=True)
    customer_name = models.CharField("客户名称", max_length=100)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.order_no
