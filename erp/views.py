from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import SalesOrder, WorkOrder

def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username","")
        p = request.POST.get("password","")
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"error":"账号或密码错误"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/login/")

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "so_count": SalesOrder.objects.count(),
        "wo_count": WorkOrder.objects.count(),
    })

@login_required
def sales_order_list(request):
    rows = SalesOrder.objects.order_by("-created_at")
    return render(request, "sales_order_list.html", {"rows": rows})

@login_required
def sales_order_new(request):
    if request.method == "POST":
        SalesOrder.objects.create(
            so_no=request.POST["so_no"],
            customer=request.POST["customer"],
            dn=request.POST["dn"],
            qty=int(request.POST["qty"]),
            contract_file=request.FILES.get("contract_file"),
            drawing_file=request.FILES.get("drawing_file"),
        )
        return redirect("/erp/sales/")
    return render(request, "sales_order_form.html")

@login_required
def work_order_list(request):
    rows = WorkOrder.objects.select_related("sales_order").order_by("-id")
    return render(request, "work_order_list.html", {"rows": rows})

@login_required
def work_order_new(request):
    if request.method == "POST":
        so = SalesOrder.objects.get(id=int(request.POST["sales_order_id"]))
        wo = WorkOrder.objects.create(
            sales_order=so,
            process=request.POST.get("process","机加工"),
            status=request.POST.get("status","待加工"),
            inspect_report=request.FILES.get("inspect_report"),
        )
        if wo.status == "已完成":
            wo.finished_at = timezone.now()
            wo.save()
        return redirect("/erp/work/")
    sos = SalesOrder.objects.order_by("-created_at")
    return render(request, "work_order_form.html", {"sales_orders": sos})
