from django.apps import AppConfig
import os
import logging

logger = logging.getLogger(__name__)


class ErpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "erp"

    def ready(self):
        """
        启动时自动创建超级管理员（方案 A）
        - 仅在数据库可用时执行
        - 已存在 admin 则跳过
        - 完全兼容 Render（无 Shell / 免费版）
        """
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            admin_username = os.environ.get("ADMIN_USER", "admin")
            admin_password = os.environ.get("ADMIN_PASSWORD", "123456")
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")

            if not User.objects.filter(username=admin_username).exists():
                User.objects.create_superuser(
                    username=admin_username,
                    password=admin_password,
                    email=admin_email,
                )
                logger.info(f"✅ 自动创建超级管理员: {admin_username}")
            else:
                logger.info("ℹ️ 超级管理员已存在，跳过创建")

        except Exception as e:
            # ⚠️ 不能 raise，否则 Render 会直接判定启动失败
            logger.warning(f"⚠️ 自动创建管理员跳过（数据库未就绪）: {e}")
