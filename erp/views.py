# erp/views.py
import os

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


def _common_ctx(request):
    """
    全站通用上下文：公司名、debug、默认管理员账号提示等
    """
    return {
        "company_name": getattr(settings, "COMPANY_NAME", os.environ.get("COMPANY_NAME", "ERP 系统")),
        "debug": getattr(settings, "DEBUG", False),
        "admin_user": os.environ.get("ADMIN_USER", "admin"),
        "admin_email": os.environ.get("ADMIN_EMAIL", "admin@example.com"),
    }


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    登录页：GET 显示表单；POST 校验账号密码
    """
    if request.user.is_authenticated:
        return redirect("/")

    error = ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 支持 next 跳转
            next_url = request.GET.get("next") or "/"
            return redirect(next_url)
        error = "账号或密码错误，请重试。"

    ctx = _common_ctx(request)
    ctx.update({"error": error})
    return render(request, "login.html", ctx)


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    退出：允许 GET/POST，修复你日志里反复出现的 405 (GET /logout/)
    """
    logout(request)
    return redirect("/login/")


@login_required
def dashboard(request):
    """
    仪表盘：先做占位，后续接 PostgreSQL 真实统计再补。
    """
    ctx = _common_ctx(request)
    ctx.update(
        {
            "kpi_today": "-",        # 今日访问
            "kpi_orders": "-",       # 订单数
            "kpi_workorders": "-",   # 工单数
            "kpi_stock_alert": "-",  # 库存预警
        }
    )
    return render(request, "dashboard.html", ctx)
