from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Ensure admin user exists"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("ADMIN_USER", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "123456")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"ℹ️ 管理员已存在: {username}")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(f"✅ 已自动创建管理员: {username}")
