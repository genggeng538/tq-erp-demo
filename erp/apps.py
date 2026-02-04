from django.apps import AppConfig

class ErpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "erp"

    def ready(self):
        # 只在 Render / 生产环境执行
        if os.environ.get("RUN_AUTO_MIGRATE") != "1":
            return

        # 防止重复执行
        if os.environ.get("AUTO_MIGRATE_DONE") == "1":
            return

        try:
            from django.core.management import call_command
            call_command("migrate", interactive=False)
            os.environ["AUTO_MIGRATE_DONE"] = "1"
            print("[AUTO MIGRATE] migrate executed successfully")
        except Exception as e:
            print("[AUTO MIGRATE ERROR]", e)
