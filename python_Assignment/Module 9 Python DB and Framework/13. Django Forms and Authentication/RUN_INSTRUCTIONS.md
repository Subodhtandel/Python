# How to Run the Django Project

## Step-by-Step Instructions

### 1. Open Terminal/Command Prompt
- Open PowerShell, Command Prompt, or your terminal
- Navigate to the project directory

### 2. Navigate to the Project Directory
```bash
cd "D:\PYTHON\python_Assignment\Module 9 Python DB and Framework\13. Django Forms and Authentication"
```

Or if you're already in the `python_Assignment` folder:
```bash
cd "Module 9 Python DB and Framework\13. Django Forms and Authentication"
```

### 3. (Optional) Create and Activate Virtual Environment
If you want to use a virtual environment (recommended):

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**
- On Windows (PowerShell):
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- On Windows (Command Prompt):
  ```bash
  venv\Scripts\activate.bat
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Django (>=5.2.8)
- Pillow (>=10.0.0) - for image handling

### 5. Run Database Migrations
Create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optional) Create a Superuser (for Admin Access)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 7. Start the Development Server
```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 8. Access the Application
Open your web browser and go to:
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### 9. Stop the Server
Press `Ctrl+C` in the terminal to stop the development server.

---

## Quick Start (All Commands at Once)

If you're running it for the first time:

```bash
# Navigate to directory
cd "D:\PYTHON\python_Assignment\Module 9 Python DB and Framework\13. Django Forms and Authentication"

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

If you've already run migrations before, you only need:

```bash
# Navigate to directory
cd "D:\PYTHON\python_Assignment\Module 9 Python DB and Framework\13. Django Forms and Authentication"

# Start server
python manage.py runserver
```

---

## Available URLs

Once the server is running, you can access:

- **Home**: http://127.0.0.1:8000/
- **Sign Up**: http://127.0.0.1:8000/signup/
- **Login**: http://127.0.0.1:8000/login/
- **Profile**: http://127.0.0.1:8000/profile/ (requires login)
- **Update Profile**: http://127.0.0.1:8000/profile/update/ (requires login)
- **Password Reset**: http://127.0.0.1:8000/password-reset/
- **Admin**: http://127.0.0.1:8000/admin/ (requires superuser)

---

## Troubleshooting

### If you get "ModuleNotFoundError: No module named 'django'"
- Make sure Django is installed: `pip install -r requirements.txt`
- If using a virtual environment, make sure it's activated

### If you get "Port 8000 is already in use"
- The server might already be running
- Use a different port: `python manage.py runserver 8001`
- Or stop the existing server (Ctrl+C in that terminal)

### If you get migration errors
- Try: `python manage.py makemigrations accounts`
- Then: `python manage.py migrate`

### If static files warning appears
- This is normal in development - the static directory will be created automatically
- You can ignore this warning


