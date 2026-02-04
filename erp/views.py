# erp/views.py
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from django.db import models
from .models import SalesOrder, WorkOrder, InventoryItem


def _company_name():
    return getattr(settings, "COMPANY_NAME", os.environ.get("COMPANY_NAME", "ERP 系统"))


@csrf_protect
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
            return redirect("/")
        error = "账号或密码错误，请重试。"

    return render(request, "login.html", {"error": error, "company_name": _company_name()})


def logout_view(request):
    # 允许 GET 退出，避免你日志里一直 405
    logout(request)
    return redirect("/login/")


@login_required
def dashboard(request):
    ctx = {
        "company_name": _company_name(),
        "kpi_today": "-",       # 你后续要真统计我再接数据库
        "kpi_orders": SalesOrder.objects.count(),
        "kpi_stock_alert": InventoryItem.objects.filter(qty_on_hand__lt=models.F("min_qty")).count()
        if InventoryItem.objects.exists()
        else 0,
    }
    return render(request, "dashboard.html", ctx)


@login_required
def so_list(request):
    qs = SalesOrder.objects.all()[:200]
    return render(request, "so_list.html", {"company_name": _company_name(), "rows": qs})


@login_required
def wo_list(request):
    qs = WorkOrder.objects.select_related("so").all()[:200]
    return render(request, "wo_list.html", {"company_name": _company_name(), "rows": qs})


@login_required
def inv_list(request):
    qs = InventoryItem.objects.all()[:500]
    return render(request, "inv_list.html", {"company_name": _company_name(), "rows": qs})
