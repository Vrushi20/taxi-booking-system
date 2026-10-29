from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import AdminProfile


class AdminRegistrationForm(UserCreationForm):
    """Registration form with Django's built-in password validation."""

    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if AdminProfile.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An admin account already uses this email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["full_name"].strip()
        user.email = self.cleaned_data["email"].strip()
        user.is_staff = True

        if commit:
            user.save()
            AdminProfile.objects.create(
                user=user,
                full_name=self.cleaned_data["full_name"].strip(),
                email=self.cleaned_data["email"].strip(),
            )
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "Email address"})
    )


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "Email address"})
    )
    otp = forms.CharField(
        label="One-time code",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={"autocomplete": "one-time-code", "inputmode": "numeric", "placeholder": "6-digit code"}
        ),
    )
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_otp(self):
        otp = self.cleaned_data["otp"]
        if not otp.isdigit():
            raise forms.ValidationError("Enter the six-digit code from the server email output.")
        return otp

    def clean_new_password(self):
        password = self.cleaned_data["new_password"]
        if self.user:
            try:
                validate_password(password, user=self.user)
            except ValidationError as error:
                raise forms.ValidationError(error.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirmation = cleaned_data.get("confirm_password")
        if password and confirmation and password != confirmation:
            self.add_error("confirm_password", "The passwords do not match.")
        return cleaned_data
