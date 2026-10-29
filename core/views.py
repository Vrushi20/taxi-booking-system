from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST


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
    return render(request, "core/dashboard.html")


@require_POST
def admin_logout(request):
    logout(request)
    return redirect("core:admin_login")
