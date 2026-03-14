# Django Admin Panel Customization - Doctor Management System

A comprehensive Django project demonstrating advanced admin panel customization for managing doctor information with detailed display of specialties, availability, and other professional details.

## Features

### Admin Panel Customizations

1. **Custom List Display**
   - Doctor photos with thumbnails
   - Clickable doctor names
   - Specialty badges with colors
   - Availability status badges with color coding
   - Experience information with levels
   - Formatted consultation fees
   - Star ratings display

2. **Advanced Filtering**
   - Filter by availability status
   - Filter by active/inactive status
   - Filter by specialties
   - Filter by location (city, state)
   - Filter by experience years
   - Date hierarchy for creation dates

3. **Detailed Search**
   - Search by name, email, phone
   - Search by license number
   - Search by specialty
   - Search by location

4. **Organized Fieldsets**
   - Personal Information section
   - Professional Information section
   - Availability & Schedule section
   - Contact Information section (collapsible)
   - Additional Information section
   - Timestamps section (collapsible)

5. **Inline Editing**
   - Weekly availability schedule (Monday-Sunday)
   - Edit schedules directly from doctor detail page

6. **Bulk Actions**
   - Mark doctors as available
   - Mark doctors as unavailable
   - Activate multiple doctors
   - Deactivate multiple doctors

7. **Custom Admin Site Headers**
   - Custom site header: "Doctor Management System"
   - Custom site title: "Doctor Admin"
   - Custom index title: "Welcome to Doctor Administration Portal"

## Models

### Specialty
- Medical specialties (Cardiology, Neurology, etc.)
- Description field
- Many-to-many relationship with doctors

### Doctor
Comprehensive doctor model with fields for:

**Personal Information:**
- First name, Last name
- Email, Phone
- Date of birth
- Profile picture

**Professional Information:**
- License number (unique)
- Specialties (many-to-many)
- Experience years
- Qualification
- Bio

**Availability:**
- Availability status (Available, Busy, On Leave, Unavailable)
- Working hours (start and end time)
- Active status

**Contact Information:**
- Address, City, State, ZIP code, Country

**Additional:**
- Consultation fee
- Rating (0-5 stars)
- Total appointments count

### AvailabilitySchedule
Weekly schedule for each doctor:
- Day of the week
- Start and end time
- Availability flag

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd "Module 9 Python DB and Framework/15. Customizing the Django Admin Panel"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows (PowerShell):
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```bash
     venv\Scripts\activate.bat
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

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Create sample data (optional):**
   ```bash
   python manage.py shell
   ```
   Then run:
   ```python
   from doctors.models import Specialty, Doctor
   
   # Create specialties
   specialties = ['Cardiology', 'Neurology', 'Dermatology', 'Orthopedics', 'Pediatrics']
   for spec in specialties:
       Specialty.objects.get_or_create(name=spec)
   
   # Create a sample doctor (adjust as needed)
   doctor = Doctor.objects.create(
       first_name='John',
       last_name='Smith',
       email='john.smith@example.com',
       phone='123-456-7890',
       license_number='DOC123456',
       experience_years=15,
       availability_status='available',
       consultation_fee=150.00,
       rating=4.5
   )
   doctor.specialties.add(Specialty.objects.get(name='Cardiology'))
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the admin panel:**
   - Admin: http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

## Usage

### Adding a Doctor

1. Log in to the admin panel
2. Click on "Doctors" under the DOCTORS section
3. Click "Add Doctor" button
4. Fill in the form:
   - Upload a profile picture (optional)
   - Enter personal information
   - Select one or more specialties
   - Set availability status and working hours
   - Add contact information
   - Set consultation fee and other details
5. Scroll down to "Availability Schedules" to set weekly schedule
6. Click "Save"

### Viewing Doctors

The list view displays:
- Photo thumbnail
- Full name (clickable to edit)
- Specialties as colored badges
- Availability status with color coding
- Experience information
- Consultation fee
- Star rating
- Active status
- Creation date

### Filtering Doctors

Use the filters on the right sidebar:
- Filter by availability status
- Filter by active status
- Filter by specialties
- Filter by location
- Filter by experience
- Use date hierarchy at the top

### Searching

Use the search box to find doctors by:
- Name
- Email
- Phone number
- License number
- Specialty name
- City or state

### Bulk Actions

1. Select multiple doctors using checkboxes
2. Choose an action from the dropdown:
   - Mark selected doctors as available
   - Mark selected doctors as unavailable
   - Activate selected doctors
   - Deactivate selected doctors
3. Click "Go"

## Admin Customization Details

### Custom Display Methods

The admin uses several custom methods to format data:

- `doctor_photo()` - Displays thumbnail in list view
- `full_name_with_title()` - Clickable name with email
- `specialties_list()` - Colored badge display
- `availability_status_badge()` - Status with color coding
- `experience_info()` - Years with level
- `consultation_fee_display()` - Formatted currency
- `rating_display()` - Star rating visualization

### Color Coding

- **Availability Status:**
  - Available: Green (#28a745)
  - Busy: Yellow/Orange (#ffc107)
  - On Leave: Blue (#17a2b8)
  - Unavailable: Red (#dc3545)

- **Experience Levels:**
  - Senior (20+ years): Green
  - Experienced (10-19 years): Blue
  - Mid-level (5-9 years): Yellow
  - Junior (0-4 years): Gray

## Project Structure

```
15. Customizing the Django Admin Panel/
├── doctor_admin_project/     # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── doctors/                   # Doctors app
│   ├── __init__.py
│   ├── admin.py              # Customized admin interface
│   ├── apps.py
│   ├── models.py             # Doctor, Specialty, AvailabilitySchedule models
│   ├── migrations/
│   └── tests.py
├── manage.py
├── requirements.txt
└── README.md
```

## Key Admin Customizations Explained

1. **list_display**: Controls what columns appear in the list view
2. **list_filter**: Adds filter options in the sidebar
3. **search_fields**: Enables search functionality
4. **fieldsets**: Organizes fields into logical groups
5. **readonly_fields**: Makes certain fields read-only
6. **inlines**: Allows editing related models inline
7. **actions**: Provides bulk operations
8. **date_hierarchy**: Adds date-based navigation
9. **list_per_page**: Controls pagination
10. **ordering**: Sets default ordering

## Technologies Used

- Django 5.2.8
- Pillow (for image handling)
- SQLite (default database)

## Notes

- This is a development project. For production:
  - Change `SECRET_KEY` in settings.py
  - Set `DEBUG = False`
  - Configure `ALLOWED_HOSTS`
  - Use a production database (PostgreSQL, MySQL)
  - Configure static files serving
  - Set up media files storage (AWS S3, etc.)

## License

This project is for educational purposes.


