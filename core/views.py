import random
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    AdminRegistrationForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
)
from .models import PasswordResetOTP


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


def forgot_password(request):
    form = PasswordResetRequestForm(request.POST or None)
    submitted = False

    if request.method == "POST" and form.is_valid():
        submitted = True
        email = form.cleaned_data["email"].strip()
        admin_user = (
            get_user_model()
            .objects.filter(email__iexact=email, is_staff=True, is_active=True)
            .order_by("pk")
            .first()
        )

        # Keep the response the same whether or not the email belongs to an account.
        if admin_user:
            otp = str(random.randint(100000, 999999))
            now = timezone.now()
            PasswordResetOTP.objects.update_or_create(
                user=admin_user,
                defaults={
                    "otp_hash": make_password(otp),
                    "created_at": now,
                    "expires_at": now + timedelta(minutes=10),
                    "attempts": 0,
                },
            )
            send_mail(
                subject="RideDesk password reset code",
                message=(
                    f"Your RideDesk password reset code is {otp}. "
                    "It expires in 10 minutes. If you did not request this, ignore this email."
                ),
                from_email=None,
                recipient_list=[email],
            )

    return render(request, "core/forgot_password.html", {"form": form, "submitted": submitted})


def reset_password(request):
    email = request.POST.get("email", "").strip()
    admin_user = None
    if email:
        admin_user = (
            get_user_model()
            .objects.filter(email__iexact=email, is_staff=True)
            .order_by("pk")
            .first()
        )

    form = PasswordResetConfirmForm(
        request.POST or None,
        user=admin_user,
        initial={"email": email},
    )
    if request.method == "POST" and form.is_valid():
        if not admin_user or not admin_user.is_active:
            form.add_error(None, "The email or reset code is invalid or has expired.")
        else:
            reset_record = PasswordResetOTP.objects.filter(user=admin_user).first()
            if not reset_record or reset_record.expires_at <= timezone.now():
                if reset_record:
                    reset_record.delete()
                form.add_error("otp", "This code is invalid or expired. Request a new code.")
            elif reset_record.attempts >= 5:
                reset_record.delete()
                form.add_error("otp", "Too many attempts. Request a new code and try again.")
            elif not check_password(form.cleaned_data["otp"], reset_record.otp_hash):
                reset_record.attempts += 1
                reset_record.save(update_fields=["attempts"])
                form.add_error("otp", "That code is incorrect. Check the server email output and try again.")
            else:
                with transaction.atomic():
                    user = admin_user
                    user.set_password(form.cleaned_data["new_password"])
                    user.save(update_fields=["password"])
                    reset_record.delete()
                return render(request, "core/reset_password.html", {"form": None, "complete": True})

    return render(request, "core/reset_password.html", {"form": form, "complete": False})


@require_POST
def admin_logout(request):
    logout(request)
    return redirect("core:admin_login")
