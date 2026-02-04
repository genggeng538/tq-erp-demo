from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"error": "用户名或密码错误"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
