from django.apps import AppConfig
import os
import sys


class ErpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "erp"

    def ready(self):
        """
        方案 A：
        Django 启动时自动创建超级管理员（只创建一次）
        """

        # 防止 migrate / collectstatic / shell 等命令时重复执行
        if "runserver" not in sys.argv and "gunicorn" not in sys.argv:
            return

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            admin_user = os.environ.get("ADMIN_USER", "admin")
            admin_password = os.environ.get("ADMIN_PASSWORD", "123456")
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")

            if not User.objects.filter(username=admin_user).exists():
                User.objects.create_superuser(
                    username=admin_user,
                    email=admin_email,
                    password=admin_password,
                )
                print(f"✅ 自动创建超级管理员：{admin_user}")
            else:
                print(f"ℹ️ 超级管理员已存在：{admin_user}")

        except Exception as e:
            # 任何异常都不影响 Django 启动
            print("⚠️ 自动创建管理员失败（已忽略）：", e)
