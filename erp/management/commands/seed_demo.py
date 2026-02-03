from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erp.models import SalesOrder, WorkOrder
import os

class Command(BaseCommand):
    help = "Seed demo data and admin user."

    def handle(self, *args, **kwargs):
        admin_user = os.environ.get("ADMIN_USER", "admin")
        admin_password = os.environ.get("ADMIN_PASSWORD", "123456")

        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(admin_user, "admin@example.com", admin_password)
            self.stdout.write(self.style.SUCCESS(f"Created admin: {admin_user}"))

        if SalesOrder.objects.count() == 0:
            so = SalesOrder.objects.create(so_no="SO-0001", customer="示例客户", dn="DN250", qty=1)
            WorkOrder.objects.create(sales_order=so, process="机加工", status="待加工")
            self.stdout.write(self.style.SUCCESS("Seeded demo SO/WO"))
