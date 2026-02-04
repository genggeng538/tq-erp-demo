# erp/views.py
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def _common_ctx(request):
    return {
        "company_name": getattr(settings, "COMPANY_NAME", os.environ.get("COMPANY_NAME", "ERP 系统")),
        "debug": bool(getattr(settings, "DEBUG", False)),
        "admin_user": os.environ.get("ADMIN_USER", "admin"),
    }


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "登录成功。")
            return redirect("/")
        messages.error(request, "账号或密码错误，请重试。")

    # 统一用 base.html 的风格：messages 显示，不再用 error 字符串
    return render(request, "login.html", _common_ctx(request))


def logout_view(request):
    logout(request)
    messages.info(request, "已退出登录。")
    return redirect("/login/")


@login_required
def dashboard(request):
    # 先占位，后续我再给你接 PostgreSQL 真实统计
    ctx = {
        **_common_ctx(request),
        "kpi_today": "—",       # 今日访问
        "kpi_orders": "—",      # 订单数
        "kpi_workorders": "—",  # 工单数（模板用这个名字）
    }
    return render(request, "dashboard.html", ctx)
