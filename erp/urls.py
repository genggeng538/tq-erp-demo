# erp/urls.py
from django.urls import path
from .views import login_view, logout_view, dashboard, so_list, wo_list, inv_list

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("so/", so_list, name="so_list"),
    path("wo/", wo_list, name="wo_list"),
    path("inv/", inv_list, name="inv_list"),
]
