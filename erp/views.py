from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required


def table_exists(table_name: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = %s
            );
            """,
            [table_name],
        )
        return cursor.fetchone()[0]


@login_required
def index(request):
    context = {}

    if table_exists("erp_salesorder"):
        from .models import SalesOrder

        context["order_count"] = SalesOrder.objects.count()
    else:
        # 数据库尚未初始化
        context["order_count"] = 0
        context["db_not_ready"] = True

    return render(request, "index.html", context)
