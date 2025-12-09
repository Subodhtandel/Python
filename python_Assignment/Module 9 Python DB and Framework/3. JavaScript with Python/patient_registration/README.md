Patient Registration Django Project

This small Django project demonstrates client-side JavaScript validation for a patient registration form.

Quick start:

1. Create and activate a virtualenv (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django
```

2. From project root run migrations:

```powershell
cd "D:\PYTHON\python_Assignment\Module 9 Python DB and Framework\3. JavaScript with Python\patient_registration"
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser (optional):

```powershell
python manage.py createsuperuser
```

4. Run the server:

```powershell
python manage.py runserver
```

5. Open `http://127.0.0.1:8000/` to access the registration form.

Notes:
- JavaScript files are under `static/js/`:
  - `validate_email.js`
  - `validate_password.js`
  - `validate_form.js`
- This demo stores passwords in plain text for simplicity — do NOT do this in production. Use Django's auth system for real projects.
