from django.contrib import admin
from .models import SalesOrder, WorkOrder

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("so_no", "customer", "dn", "qty", "created_at")
    search_fields = ("so_no", "customer")

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("sales_order", "process", "status", "finished_at")
    list_filter = ("status", "process")
