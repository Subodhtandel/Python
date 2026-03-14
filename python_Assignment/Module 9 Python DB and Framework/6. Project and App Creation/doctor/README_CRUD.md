# Django CRUD Operations - Doctor Profiles

This Django project demonstrates complete CRUD (Create, Read, Update, Delete) operations on doctor profiles using Django ORM.

## Quick Start

1. **Run the demo command:**
   ```bash
   python manage.py demo_crud
   ```

2. **Access the web interface:**
   ```bash
   python manage.py runserver
   ```
   Then visit: `http://127.0.0.1:8000/doctors/`

## CRUD Operations Overview

### ✅ CREATE
- **URL:** `/doctors/new/`
- **View:** `doctor_create`
- **ORM Method:** `Doctor.objects.create()` or `form.save()`
- **Example:**
  ```python
  doctor = Doctor.objects.create(
      first_name='John',
      last_name='Smith',
      email='john@example.com',
      phone='123-456-7890',
      specialization='cardiology',
      license_number='LIC001',
      experience_years=10
  )
  ```

### 📖 READ
- **List:** `/doctors/` - `Doctor.objects.all()`
- **Detail:** `/doctors/<id>/` - `Doctor.objects.get(pk=id)`
- **Filter:** `Doctor.objects.filter(specialization='cardiology')`
- **Example:**
  ```python
  # Get all doctors
  all_doctors = Doctor.objects.all()
  
  # Get single doctor
  doctor = Doctor.objects.get(pk=1)
  
  # Filter doctors
  cardiologists = Doctor.objects.filter(specialization='cardiology')
  ```

### ✏️ UPDATE
- **URL:** `/doctors/<id>/edit/`
- **View:** `doctor_update`
- **ORM Method:** `doctor.save()` or `Doctor.objects.filter().update()`
- **Example:**
  ```python
  # Update single record
  doctor = Doctor.objects.get(pk=1)
  doctor.experience_years = 15
  doctor.save()
  
  # Bulk update
  Doctor.objects.filter(specialization='cardiology').update(is_available=False)
  ```

### 🗑️ DELETE
- **URL:** `/doctors/<id>/delete/`
- **View:** `doctor_delete`
- **ORM Method:** `doctor.delete()` or `Doctor.objects.filter().delete()`
- **Example:**
  ```python
  # Delete single record
  doctor = Doctor.objects.get(pk=1)
  doctor.delete()
  
  # Bulk delete
  Doctor.objects.filter(specialization='general').delete()
  ```

## Files Structure

```
doctor/
├── myapp/
│   ├── models.py              # Doctor model definition
│   ├── views.py               # CRUD views with ORM operations
│   ├── forms.py               # DoctorForm for create/update
│   ├── urls.py                # URL routing
│   ├── admin.py               # Django admin configuration
│   └── management/
│       └── commands/
│           └── demo_crud.py  # Demo command
├── CRUD_OPERATIONS.md         # Detailed ORM documentation
└── README_CRUD.md            # This file
```

## Key Features

1. **Complete CRUD Implementation**
   - All operations use Django ORM
   - Proper error handling with `get_object_or_404()`
   - Form validation

2. **Django ORM Methods Demonstrated:**
   - `objects.create()` - Create records
   - `objects.all()` - Get all records
   - `objects.get()` - Get single record
   - `objects.filter()` - Filter records
   - `save()` - Update records
   - `delete()` - Delete records
   - `objects.update()` - Bulk update
   - `objects.count()` - Count records

3. **Advanced Features:**
   - Filtering by specialization
   - Filtering by availability
   - Search functionality
   - Related object access (appointments)

## Testing CRUD Operations

### Using Django Shell

```bash
python manage.py shell
```

```python
from myapp.models import Doctor

# CREATE
doctor = Doctor.objects.create(
    first_name='Test',
    last_name='Doctor',
    email='test@example.com',
    phone='123-456-7890',
    specialization='cardiology',
    license_number='TEST001',
    experience_years=5
)

# READ
all_doctors = Doctor.objects.all()
doctor = Doctor.objects.get(pk=1)

# UPDATE
doctor.experience_years = 10
doctor.save()

# DELETE
doctor.delete()
```

### Using Management Command

```bash
python manage.py demo_crud
```

This command demonstrates all CRUD operations with sample data.

## URL Routes

| Operation | URL | View Function |
|-----------|-----|---------------|
| List | `/doctors/` | `doctor_list` |
| Detail | `/doctors/<id>/` | `doctor_detail` |
| Create | `/doctors/new/` | `doctor_create` |
| Update | `/doctors/<id>/edit/` | `doctor_update` |
| Delete | `/doctors/<id>/delete/` | `doctor_delete` |

## Documentation

- **CRUD_OPERATIONS.md** - Comprehensive guide with all ORM examples
- **DATABASE_SETUP.md** - Database configuration guide
- **This file** - Quick reference guide

## Model Fields

The Doctor model includes:
- `first_name`, `last_name` - Personal information
- `email` - Unique email address
- `phone` - Contact number
- `specialization` - Medical specialization
- `license_number` - Unique license identifier
- `experience_years` - Years of experience
- `is_available` - Availability status
- `created_at`, `updated_at` - Timestamps

## Best Practices Demonstrated

1. ✅ Using `get_object_or_404()` instead of `get()`
2. ✅ Form validation before saving
3. ✅ Proper error handling
4. ✅ Using `bulk_create()` and `update()` for efficiency
5. ✅ Related object access through ForeignKey
6. ✅ Query optimization with filtering

## Next Steps

1. Review `CRUD_OPERATIONS.md` for detailed examples
2. Run `python manage.py demo_crud` to see CRUD in action
3. Explore the web interface at `/doctors/`
4. Try creating, updating, and deleting doctors through the UI

---

**Project:** Doctor Management System  
**Django Version:** 5.2.8  
**Database:** SQLite (configurable to MySQL/PostgreSQL)



