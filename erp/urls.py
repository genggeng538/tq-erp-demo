from django.urls import path
from . import views

urlpatterns = [
    path("sales/", views.sales_order_list, name="sales_list"),
    path("sales/new/", views.sales_order_new, name="sales_new"),
    path("work/", views.work_order_list, name="work_list"),
    path("work/new/", views.work_order_new, name="work_new"),
]
