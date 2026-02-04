import os
import logging

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError


logger = logging.getLogger(__name__)


class ErpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "erp"

    def ready(self):
        """
        Auto-create a superuser on startup (works on Render free plan without Shell).
        Controlled by env vars:
          - ADMIN_USER (default: admin)
          - ADMIN_PASSWORD (default: 123456)
          - ADMIN_EMAIL (default: admin@example.com)
          - AUTO_CREATE_ADMIN (default: 1) -> set to 0 to disable
          - FORCE_ADMIN_PASSWORD (default: 0) -> set to 1 to reset password on every boot
        """

        if os.environ.get("AUTO_CREATE_ADMIN", "1") != "1":
            return

        username = os.environ.get("ADMIN_USER", "admin").strip()
        password = os.environ.get("ADMIN_PASSWORD", "123456").strip()
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com").strip()

        if not username or not password:
            logger.warning("AUTO_CREATE_ADMIN enabled but ADMIN_USER/ADMIN_PASSWORD missing.")
            return

        try:
            conn = connections["default"]
            conn.ensure_connection()

            # Ensure auth table exists (avoid errors during first migrate/build)
            table_names = conn.introspection.table_names()
            User = get_user_model()
            if User._meta.db_table not in table_names:
                # DB not migrated yet; skip silently
                return

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            changed = False

            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.email = email
                user.save()
                logger.warning(f"[AUTO_CREATE_ADMIN] Superuser created: {username}")
                return

            # If already exists, ensure permissions are correct
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if email and user.email != email:
                user.email = email
                changed = True

            # Optionally force-reset password every boot
            if os.environ.get("FORCE_ADMIN_PASSWORD", "0") == "1":
                user.set_password(password)
                changed = True

            if changed:
                user.save()
                logger.warning(f"[AUTO_CREATE_ADMIN] Superuser updated: {username}")

        except (OperationalError, ProgrammingError):
            # DB not ready yet (e.g., during build); ignore and let next boot handle it
            return
        except Exception as e:
            logger.exception(f"[AUTO_CREATE_ADMIN] Unexpected error: {e}")
            return
