from django.contrib import admin
from .models import SalesOrder


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("order_no", "customer_name", "created_at")
    search_fields = ("order_no", "customer_name")
