# Doctor Profile Page - Django Project

## Project Description
This is a Django web application that displays a doctor profile page with custom CSS styling. It includes a doctor listing page and individual doctor detail pages with professional styling.

## Features
- **Doctor Listing Page**: Display multiple doctors in a responsive grid layout
- **Doctor Detail Page**: View complete doctor profile with contact information
- **Custom CSS Styling**: Modern, professional design with gradient backgrounds and animations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Django Admin**: Manage doctors through Django admin interface

## Project Structure
```
doctor_project/
├── manage.py                 # Django management script
├── db.sqlite3               # Database file
├── doctor_project/          # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
├── doctor_app/              # Main application
│   ├── models.py            # Doctor model
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   └── apps.py              # App configuration
├── templates/               # HTML templates
│   └── doctor/
│       ├── doctor_list.html      # Listing page
│       └── doctor_detail.html    # Detail page
└── static/                  # Static files
    └── css/
        └── style.css        # Main CSS styling (650+ lines)
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django
```

### 2. Navigate to Project Directory
```bash
cd doctor_project
```

### 3. Create Database
```bash
python manage.py migrate
```

### 4. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 5. Add Sample Data (through Django Admin)
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/admin` and login with your superuser credentials.

Add sample doctors through the Doctor section.

## Running the Application

```bash
python manage.py runserver
```

Then visit:
- **Doctor List**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## CSS Features

### Color Scheme
- **Primary Gradient**: Purple (#667eea) to Dark Purple (#764ba2)
- **Accent**: Gold/Yellow (#ffc107) for ratings
- **Background**: Light Gray (#f8f9fa)

### Components
1. **Header Section**: Gradient background with title and subtitle
2. **Search Bar**: Rounded search input with shadow effects
3. **Doctor Cards**: Hover animations and gradient borders
4. **Profile Cards**: Detailed layout with organized sections
5. **Buttons**: Multiple button styles (primary, secondary, outline)
6. **Contact Section**: Icon-based contact information
7. **Rating Display**: Star-based rating system

### Animations
- Slide down animation for header
- Fade in up animation for cards
- Smooth hover effects on interactive elements
- Transform animations on buttons

### Responsive Breakpoints
- **Desktop**: Full grid layout
- **Tablet**: Adjusted grid columns
- **Mobile**: Single column layout with full-width buttons

## Data Model

### Doctor Model
```python
- name: CharField (max_length=100)
- specialization: CharField (max_length=100)
- experience: IntegerField
- phone: CharField (max_length=20)
- email: EmailField
- location: CharField (max_length=200)
- bio: TextField
- rating: FloatField (default=4.5)
- created_at: DateTimeField (auto_now_add=True)
```

## Sample Doctor Data

You can add this data through the Django admin:

**Doctor 1:**
- Name: Dr. Sarah Johnson
- Specialization: Cardiology
- Experience: 12 years
- Phone: +1-555-0101
- Email: sarah.johnson@hospital.com
- Location: New York, NY
- Bio: Expert cardiologist with over 12 years of experience in treating heart diseases and cardiac rehabilitation.
- Rating: 4.8

**Doctor 2:**
- Name: Dr. Michael Chen
- Specialization: Neurology
- Experience: 15 years
- Phone: +1-555-0102
- Email: michael.chen@hospital.com
- Location: San Francisco, CA
- Bio: Renowned neurologist specializing in neurological disorders and advanced treatment techniques.
- Rating: 4.9

## Technology Stack
- **Backend**: Django 5.2+
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3
- **Python**: 3.10+

## Files Overview

### settings.py
- Configures Django apps, middleware, templates, and static files
- Sets up SQLite database
- Enables DEBUG mode for development

### models.py
- Defines Doctor model with all necessary fields
- Includes `__str__` method for admin display

### views.py
- `doctor_list()`: Returns all doctors for listing page
- `doctor_detail()`: Returns specific doctor detail

### style.css
- 650+ lines of custom CSS
- Comprehensive styling for all components
- Mobile-first responsive design
- Gradient backgrounds and animations
- Modern UI elements and hover effects

## Customization

### Changing Colors
Edit the gradient values in `static/css/style.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding More Doctors
1. Go to `/admin/`
2. Click "Add Doctor"
3. Fill in all fields
4. Save

### Modifying Templates
Edit `templates/doctor/doctor_list.html` or `templates/doctor/doctor_detail.html`

## Notes
- Static files are configured to be served in DEBUG mode
- All CSS is included in a single `style.css` file for simplicity
- No external CSS libraries required (pure vanilla CSS)
- Fully responsive and modern design
