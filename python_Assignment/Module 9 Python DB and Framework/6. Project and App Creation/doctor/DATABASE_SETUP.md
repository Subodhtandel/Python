# Database Setup Guide - Doctor Management System

This guide explains how to configure and use SQLite and MySQL databases with the Doctor Management System.

## Current Database Configuration

The project is currently configured to use **SQLite** by default, which requires no additional setup.

## Database Options

### 1. SQLite (Default - Currently Active)

**Advantages:**
- No installation required
- Perfect for development and small applications
- Database stored in a single file
- Zero configuration

**Configuration:**
Already configured in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Location:** `db.sqlite3` in the project root directory

---

### 2. MySQL

**Advantages:**
- Better for production environments
- Supports concurrent connections
- Better performance for large datasets
- Advanced features and scalability

#### Setup Steps:

1. **Install MySQL Server**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Or use: `sudo apt-get install mysql-server` (Linux)
   - Or use: `brew install mysql` (macOS)

2. **Create MySQL Database**
   ```sql
   CREATE DATABASE doctor_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON doctor_management.* TO 'your_username'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Install MySQL Client for Python**
   ```bash
   pip install mysqlclient
   ```
   Or alternatively:
   ```bash
   pip install pymysql
   ```

4. **Update settings.py**
   Uncomment and configure the MySQL section in `doctor/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'doctor_management',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'charset': 'utf8mb4',
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       }
   }
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

### 3. PostgreSQL (Alternative)

**Advantages:**
- Advanced features
- Excellent for complex queries
- Strong data integrity
- Open source

#### Setup Steps:

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/

2. **Create Database**
   ```sql
   CREATE DATABASE doctor_management;
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE doctor_management TO your_username;
   ```

3. **Install PostgreSQL Adapter**
   ```bash
   pip install psycopg2-binary
   ```

4. **Update settings.py**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'doctor_management',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## Database Management Commands

### Create Migrations
```bash
python manage.py makemigrations
```
Creates migration files based on model changes.

### Apply Migrations
```bash
python manage.py migrate
```
Applies all pending migrations to the database.

### Show Migration Status
```bash
python manage.py showmigrations
```
Shows which migrations have been applied.

### Database Shell
```bash
python manage.py dbshell
```
Opens an interactive database shell (SQLite/MySQL/PostgreSQL).

### Create Superuser
```bash
python manage.py createsuperuser
```
Creates an admin user for Django admin interface.

---

## Doctor Record Management

### Models

The system includes the following models:

1. **Doctor Model**
   - Fields: first_name, last_name, email, phone, specialization, license_number, experience_years, is_available
   - Relationships: Has many appointments

2. **Appointment Model**
   - Fields: doctor (ForeignKey), patient_name, patient_email, appointment_date, reason, status, notes
   - Relationships: Belongs to a doctor

3. **Patient Model**
   - Fields: first_name, last_name, email, phone, date_of_birth, address
   - Used for patient registration

### CRUD Operations

#### Create Doctor
- URL: `/doctors/new/`
- View: `doctor_create`
- Form: `DoctorForm`

#### Read/List Doctors
- URL: `/doctors/`
- View: `doctor_list`
- Displays all doctors with filtering options

#### View Doctor Details
- URL: `/doctors/<id>/`
- View: `doctor_detail`
- Shows full doctor profile

#### Update Doctor
- URL: `/doctors/<id>/edit/`
- View: `doctor_update`
- Form: `DoctorForm` (with instance)

#### Delete Doctor
- URL: `/doctors/<id>/delete/`
- View: `doctor_delete`
- Requires confirmation

---

## Database Information Page

Access the database information page at: `/database/`

This page displays:
- Database connection status
- Database type and configuration
- Statistics (doctors, appointments, patients)
- Recent doctor records
- Specialization breakdown

---

## Switching Between Databases

### From SQLite to MySQL:

1. Backup your SQLite data (if needed)
2. Configure MySQL in `settings.py`
3. Run migrations: `python manage.py migrate`
4. Load data (if you have fixtures)

### From MySQL to SQLite:

1. Export data from MySQL
2. Update `settings.py` to use SQLite
3. Delete old database file (if starting fresh)
4. Run migrations: `python manage.py migrate`
5. Import data

---

## Troubleshooting

### MySQL Connection Issues

**Error: "Can't connect to MySQL server"**
- Check if MySQL service is running
- Verify host and port settings
- Check firewall settings

**Error: "Access denied for user"**
- Verify username and password
- Check user privileges
- Ensure user has access to the database

### SQLite Issues

**Error: "Database is locked"**
- Close other connections
- Check for long-running transactions
- Restart the application

---

## Best Practices

1. **Always backup before migrations**
2. **Use migrations for schema changes**
3. **Test database changes in development first**
4. **Use transactions for data integrity**
5. **Monitor database performance**
6. **Keep database credentials secure (use environment variables in production)**

---

## Environment Variables (Recommended for Production)

For production, use environment variables instead of hardcoding credentials:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'doctor_management'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

---

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Database-specific documentation:
  - SQLite: https://www.sqlite.org/docs.html
  - MySQL: https://dev.mysql.com/doc/
  - PostgreSQL: https://www.postgresql.org/docs/

---

**Last Updated:** 2024
**Project:** Doctor Management System
**Django Version:** 5.2.8

