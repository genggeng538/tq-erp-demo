# erp/views.py
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os

def _common_ctx(request):
    return {
        "company_name": getattr(settings, "COMPANY_NAME", os.environ.get("COMPANY_NAME", "")),
        "debug": getattr(settings, "DEBUG", False),
        "admin_user": os.environ.get("ADMIN_USER", "admin"),
    }

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    error = ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        error = "账号或密码错误，请重试。"

    return render(
        request,
        "login.html",
        {
            "error": error,
            "company_name": getattr(settings, "COMPANY_NAME", "ERP 系统"),
        },
    )


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
def dashboard(request):
    # 先占位，后续你要接真实统计我再给你补数据库统计逻辑
    ctx = {
        "company_name": getattr(settings, "COMPANY_NAME", "ERP 系统"),
        "kpi_today": "-",         # 今日访问
        "kpi_orders": "-",        # 订单数
        "kpi_stock_alert": "-",   # 库存预警
    }
    return render(request, "dashboard.html", ctx)
