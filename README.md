# RideDesk - Taxi Booking System

A Django project built in daily tasks. It uses SQLite, a `core` app, Django authentication for staff login/logout, a dashboard, a manual admin registration page, and a console-based email password-reset flow.

## Requirements

- Python 3.10 or newer
- Django, installed from `requirements.txt`

## Run locally on Windows

1. Open PowerShell in this folder and create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

2. Activate it. If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install Django and prepare the SQLite database:

   ```powershell
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

   When new model fields are added in later tasks, create and apply migrations with `python manage.py makemigrations` and `python manage.py migrate`.

4. Start the site:

   ```powershell
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/register/` to create an admin account. Registration stores profile details in the custom `AdminProfile` table and uses Django's built-in user model for authentication and password hashing. The login page is at `/`; the staff dashboard is at `/dashboard/`; password recovery starts at `/forgot-password/`. Django's built-in admin is at `/django-admin/`.

The dashboard has a responsive dropdown menu. Drivers, Users, and Bookings are display-only options; Logout is active.

## Password reset in development

The email backend is configured to print emails in the terminal running `runserver`. Request a reset at `/forgot-password/`, copy the six-digit code from the terminal, then enter it with the account email and a new password at `/reset-password/`. Codes expire after 10 minutes and are limited to five attempts. The code is stored as a hash in SQLite and removed after a successful reset.

## Main files

- `config/settings.py` contains the project configuration and SQLite database setting.
- `core/views.py` handles staff sign-in, registration, the protected dashboard, and sign-out.
- `core/models.py` defines the custom administrator profile table linked to Django's user account.
- `core/forms.py` validates registration and uses Django's password validation.
- `core/templates/core/` contains the login and dashboard pages.
- `core/static/core/styles.css` contains the page styling.

The current settings are for local development. Before deployment, set a secure `SECRET_KEY`, turn off `DEBUG`, and configure `ALLOWED_HOSTS`.
