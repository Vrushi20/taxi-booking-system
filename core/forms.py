from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
