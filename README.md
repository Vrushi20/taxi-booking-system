# RideDesk - Taxi Booking System

A Django project built in daily tasks. Day 1 sets up the Django project, SQLite database, `core` app, and a staff login page. There is no public registration page.

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

4. Create a staff account and start the site:

   ```powershell
   python manage.py createsuperuser
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/` and sign in. The staff dashboard is at `/dashboard/`. Django's built-in admin is at `/django-admin/`.

## Main files

- `config/settings.py` contains the project configuration and SQLite database setting.
- `core/views.py` handles staff sign-in, the protected dashboard, and sign-out.
- `core/templates/core/` contains the login and dashboard pages.
- `core/static/core/styles.css` contains the page styling.

The current settings are for local development. Before deployment, set a secure `SECRET_KEY`, turn off `DEBUG`, and configure `ALLOWED_HOSTS`.
