from django.db import models

class SalesOrder(models.Model):
    DN_CHOICES = [("DN200","DN200"), ("DN250","DN250"), ("DN300","DN300")]
    so_no = models.CharField("销售订单号", max_length=32, unique=True)
    customer = models.CharField("客户名称", max_length=100)
    dn = models.CharField("规格", max_length=10, choices=DN_CHOICES)
    qty = models.PositiveIntegerField("数量", default=1)
    contract_file = models.FileField("合同附件", upload_to="attachments/contracts/", blank=True, null=True)
    drawing_file = models.FileField("图纸附件", upload_to="attachments/drawings/", blank=True, null=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.so_no

class WorkOrder(models.Model):
    STATUS = [("待加工","待加工"), ("加工中","加工中"), ("待检验","待检验"), ("已完成","已完成")]
    sales_order = models.ForeignKey(SalesOrder, verbose_name="关联销售订单", on_delete=models.CASCADE)
    process = models.CharField("工序", max_length=50, default="机加工")
    status = models.CharField("状态", max_length=20, choices=STATUS, default="待加工")
    inspect_report = models.FileField("检验报告", upload_to="attachments/inspect/", blank=True, null=True)
    finished_at = models.DateTimeField("完工时间", blank=True, null=True)

    def __str__(self):
        return f"工单-{self.sales_order.so_no}"
