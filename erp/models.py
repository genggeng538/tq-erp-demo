# erp/models.py
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        abstract = True


class SalesOrder(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        CONFIRMED = "confirmed", "已确认"
        DONE = "done", "已完成"
        CANCELED = "canceled", "已取消"

    order_no = models.CharField("订单号", max_length=50, unique=True)
    customer_name = models.CharField("客户名称", max_length=100, blank=True, default="")
    contact = models.CharField("联系人/电话", max_length=100, blank=True, default="")
    remark = models.CharField("备注", max_length=200, blank=True, default="")
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = "销售订单"
        verbose_name_plural = "销售订单"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_no}({self.get_status_display()})"


class WorkOrder(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "新建"
        IN_PROGRESS = "in_progress", "生产中"
        DONE = "done", "已完工"
        CANCELED = "canceled", "已取消"

    wo_no = models.CharField("工单号", max_length=50, unique=True)
    so = models.ForeignKey(SalesOrder, verbose_name="关联销售订单", on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField("产品/项目", max_length=120, blank=True, default="")
    qty = models.DecimalField("数量", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.NEW)
    remark = models.CharField("备注", max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "生产工单"
        verbose_name_plural = "生产工单"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.wo_no}({self.get_status_display()})"


class InventoryItem(TimeStampedModel):
    class ItemType(models.TextChoices):
        MATERIAL = "material", "物料"
        PRODUCT = "product", "成品"

    sku = models.CharField("SKU/编码", max_length=50, unique=True)
    name = models.CharField("名称", max_length=120)
    item_type = models.CharField("类型", max_length=20, choices=ItemType.choices, default=ItemType.MATERIAL)
    unit = models.CharField("单位", max_length=20, blank=True, default="件")
    qty_on_hand = models.DecimalField("现存量", max_digits=14, decimal_places=2, default=0)
    min_qty = models.DecimalField("最低库存", max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "库存物料/成品"
        verbose_name_plural = "库存物料/成品"
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} - {self.name}"
