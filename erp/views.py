from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    stats = {
        "visits": "-",
        "orders": "-",
        "workorders": "-",
        "stock_alerts": "-",
    }
    return render(request, "dashboard.html", {"stats": stats})
