# erp/admin.py
from django.contrib import admin
from .models import SalesOrder, WorkOrder, InventoryItem


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("order_no", "customer_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("order_no", "customer_name")


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("wo_no", "so", "product_name", "qty", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("wo_no", "product_name", "so__order_no")


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "item_type", "qty_on_hand", "min_qty", "unit", "updated_at")
    list_filter = ("item_type",)
    search_fields = ("sku", "name")
