# Django User Authentication System

A complete Django project for handling user signup, login, password reset, and profile management.

## Features

- **User Signup**: Create new user accounts with email, username, and password
- **User Login**: Secure authentication with username and password
- **Password Reset**: Email-based password recovery system
- **Profile Management**: View and update user profile information
- **Extended User Profile**: Additional fields like phone number, address, bio, profile picture, and date of birth

## Project Structure

```
13. Django Forms and Authentication/
├── auth_project/          # Main Django project
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── accounts/              # Authentication app
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py
│   ├── forms.py           # Custom forms for authentication
│   ├── models.py          # UserProfile model
│   ├── urls.py            # App URL patterns
│   └── views.py           # View functions
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── accounts/          # Account-related templates
│       ├── home.html
│       ├── signup.html
│       ├── login.html
│       ├── profile.html
│       ├── profile_update.html
│       ├── password_reset.html
│       ├── password_reset_done.html
│       ├── password_reset_confirm.html
│       ├── password_reset_complete.html
│       ├── password_reset_email.html
│       └── password_reset_subject.txt
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd "Module 9 Python DB and Framework/13. Django Forms and Authentication"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

### User Signup
1. Navigate to the home page or signup page
2. Fill in the registration form with:
   - Username
   - Email address
   - First name (optional)
   - Last name (optional)
   - Password
   - Confirm password
3. Click "Sign Up"
4. You'll be redirected to the login page

### User Login
1. Go to the login page
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to your profile page

### Password Reset
1. On the login page, click "Forgot your password?"
2. Enter your email address
3. Check your email for the reset link
4. Click the link and set a new password

### Profile Management
1. After logging in, navigate to your profile
2. Click "Update Profile" to edit your information
3. You can update:
   - Email address
   - First and last name
   - Phone number
   - Address
   - Bio
   - Profile picture
   - Date of birth
4. Click "Update Profile" to save changes

## Email Configuration

For development, the project uses Django's console email backend, which prints emails to the console. 

For production, configure SMTP settings in `auth_project/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Models

### UserProfile
Extended user profile model with additional fields:
- `user`: OneToOne relationship with Django's User model
- `phone_number`: User's phone number
- `address`: User's address
- `bio`: Short biography
- `profile_picture`: User's profile image
- `date_of_birth`: User's date of birth
- `created_at`: Profile creation timestamp
- `updated_at`: Last update timestamp

## Security Notes

- This is a development project. For production:
  - Change `SECRET_KEY` in settings.py
  - Set `DEBUG = False`
  - Configure proper `ALLOWED_HOSTS`
  - Use HTTPS
  - Configure proper email backend
  - Use environment variables for sensitive settings

## Technologies Used

- Django 5.2.8
- Bootstrap 5.3.0 (for UI)
- Bootstrap Icons (for icons)
- Pillow (for image handling)
- SQLite (default database)

## License

This project is for educational purposes.



