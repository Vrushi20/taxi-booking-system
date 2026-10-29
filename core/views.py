from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db import transaction
from django.views.decorators.http import require_POST

from .forms import AdminRegistrationForm


class AdminLoginView(LoginView):
    """Manual staff login using Django's built-in authentication."""

    template_name = "core/admin_login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        # Keep the login restricted to staff/admin accounts.
        if not form.get_user().is_staff:
            form.add_error(None, "This account does not have staff access.")
            return self.form_invalid(form)
        return super().form_valid(form)


@login_required
def dashboard(request):
    profile = getattr(request.user, "admin_profile", None)
    return render(request, "core/dashboard.html", {"admin_profile": profile})


def admin_register(request):
    """Create a staff login and its custom admin profile record."""
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    form = AdminRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save()
        auth_login(request, user)
        return redirect("core:dashboard")

    return render(request, "core/admin_register.html", {"form": form})


@require_POST
def admin_logout(request):
    logout(request)
    return redirect("core:admin_login")
