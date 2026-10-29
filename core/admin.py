from django.contrib import admin
from .models import AdminProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "user", "created_at")
    search_fields = ("full_name", "email", "user__username")
