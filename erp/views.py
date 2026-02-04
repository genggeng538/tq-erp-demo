# erp/views.py
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


def _common_ctx(request):
    return {
        "company_name": getattr(settings, "COMPANY_NAME", os.environ.get("COMPANY_NAME", "ERP 系统")),
        "debug": getattr(settings, "DEBUG", False),
        "admin_user": os.environ.get("ADMIN_USER", "admin"),
        "admin_email": os.environ.get("ADMIN_EMAIL", "admin@example.com"),
        "user": request.user,
    }


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    error = ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next") or "/")
        error = "账号或密码错误"

    ctx = _common_ctx(request)
    ctx["error"] = error
    return render(request, "login.html", ctx)


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
def dashboard(request):
    ctx = _common_ctx(request)
    ctx.update({
        "kpi_today": "-",
        "kpi_orders": "-",
        "kpi_workorders": "-",
        "kpi_stock_alert": "-",
    })
    return render(request, "dashboard.html", ctx)
