from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.AdminLoginView.as_view(), name="admin_login"),
    path("register/", views.admin_register, name="admin_register"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.admin_logout, name="logout"),
]
