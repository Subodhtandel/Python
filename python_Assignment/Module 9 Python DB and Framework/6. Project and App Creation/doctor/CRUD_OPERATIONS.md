# Django CRUD Operations - Doctor Profiles

This document demonstrates CRUD (Create, Read, Update, Delete) operations on doctor profiles using Django ORM.

## Table of Contents
1. [Model Definition](#model-definition)
2. [Create Operations](#create-operations)
3. [Read Operations](#read-operations)
4. [Update Operations](#update-operations)
5. [Delete Operations](#delete-operations)
6. [Advanced ORM Queries](#advanced-orm-queries)

---

## Model Definition

### Doctor Model

```python
from django.db import models

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Practice'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, default='general')
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.get_specialization_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
```

---

## Create Operations

### 1. Using Model Constructor and save()

```python
# Create a new doctor instance
doctor = Doctor(
    first_name='John',
    last_name='Smith',
    email='john.smith@example.com',
    phone='123-456-7890',
    specialization='cardiology',
    license_number='LIC123456',
    experience_years=10,
    is_available=True
)
doctor.save()  # Saves to database
```

### 2. Using create() Method (Recommended)

```python
# Create and save in one step
doctor = Doctor.objects.create(
    first_name='Jane',
    last_name='Doe',
    email='jane.doe@example.com',
    phone='987-654-3210',
    specialization='dermatology',
    license_number='LIC789012',
    experience_years=5,
    is_available=True
)
# No need to call save() - create() saves automatically
```

### 3. Using get_or_create() (Prevents Duplicates)

```python
# Creates if doesn't exist, returns existing if it does
doctor, created = Doctor.objects.get_or_create(
    email='john.smith@example.com',
    defaults={
        'first_name': 'John',
        'last_name': 'Smith',
        'phone': '123-456-7890',
        'specialization': 'cardiology',
        'license_number': 'LIC123456',
        'experience_years': 10,
    }
)
# created is True if new record was created, False if existing
```

### 4. Using bulk_create() (Multiple Records)

```python
# Create multiple doctors at once (efficient for large datasets)
doctors = [
    Doctor(first_name='Alice', last_name='Johnson', email='alice@example.com', 
           phone='111-111-1111', specialization='neurology', license_number='LIC001', experience_years=8),
    Doctor(first_name='Bob', last_name='Williams', email='bob@example.com', 
           phone='222-222-2222', specialization='orthopedics', license_number='LIC002', experience_years=12),
    Doctor(first_name='Charlie', last_name='Brown', email='charlie@example.com', 
           phone='333-333-3333', specialization='pediatrics', license_number='LIC003', experience_years=6),
]
Doctor.objects.bulk_create(doctors)
```

### 5. Using Django Forms (In Views)

```python
# In views.py
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()  # ORM: Creates and saves doctor
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'myapp/doctor_form.html', {'form': form})
```

**URL:** `/doctors/new/`

---

## Read Operations

### 1. Get All Records

```python
# Get all doctors
all_doctors = Doctor.objects.all()
# Returns QuerySet of all Doctor objects

# Convert to list
doctors_list = list(Doctor.objects.all())

# Count records
total_doctors = Doctor.objects.count()
```

### 2. Get Single Record

```python
# Get by primary key
doctor = Doctor.objects.get(pk=1)
doctor = Doctor.objects.get(id=1)  # Same as above

# Get by unique field
doctor = Doctor.objects.get(email='john.smith@example.com')
doctor = Doctor.objects.get(license_number='LIC123456')

# Using get_object_or_404 (in views)
from django.shortcuts import get_object_or_404
doctor = get_object_or_404(Doctor, pk=1)  # Returns 404 if not found
```

### 3. Filter Records

```python
# Filter by single condition
cardiologists = Doctor.objects.filter(specialization='cardiology')

# Filter by multiple conditions (AND)
available_cardiologists = Doctor.objects.filter(
    specialization='cardiology',
    is_available=True
)

# Filter with comparison operators
experienced_doctors = Doctor.objects.filter(experience_years__gte=10)  # >= 10 years
new_doctors = Doctor.objects.filter(experience_years__lt=5)  # < 5 years

# Filter with contains (case-sensitive)
doctors_with_smith = Doctor.objects.filter(last_name__contains='Smith')

# Filter with icontains (case-insensitive)
doctors_with_john = Doctor.objects.filter(first_name__icontains='john')

# Filter with startswith
doctors_starting_with_j = Doctor.objects.filter(first_name__startswith='J')

# Filter with in
specializations = ['cardiology', 'dermatology']
doctors_in_specializations = Doctor.objects.filter(specialization__in=specializations)
```

### 4. Exclude Records

```python
# Exclude unavailable doctors
available_doctors = Doctor.objects.exclude(is_available=False)

# Exclude by multiple conditions
non_cardiologists = Doctor.objects.exclude(
    specialization='cardiology',
    experience_years__lt=5
)
```

### 5. Order Records

```python
# Order by single field (ascending)
doctors_ordered = Doctor.objects.all().order_by('first_name')

# Order by single field (descending)
doctors_desc = Doctor.objects.all().order_by('-created_at')

# Order by multiple fields
doctors_multi = Doctor.objects.all().order_by('specialization', 'last_name')

# Reverse order
doctors_reversed = Doctor.objects.all().reverse()
```

### 6. Limit and Slice

```python
# Get first 5 doctors
first_five = Doctor.objects.all()[:5]

# Get last 5 doctors
last_five = Doctor.objects.all().order_by('-id')[:5]

# Skip first 10, get next 5
doctors_11_to_15 = Doctor.objects.all()[10:15]
```

### 7. Complex Queries with Q Objects

```python
from django.db.models import Q

# OR conditions
doctors = Doctor.objects.filter(
    Q(specialization='cardiology') | Q(specialization='neurology')
)

# AND with OR
doctors = Doctor.objects.filter(
    Q(is_available=True) & (Q(experience_years__gte=10) | Q(specialization='cardiology'))
)

# NOT conditions
doctors = Doctor.objects.filter(~Q(specialization='general'))
```

### 8. Aggregations

```python
from django.db.models import Count, Avg, Max, Min, Sum

# Count by specialization
specialization_counts = Doctor.objects.values('specialization').annotate(
    count=Count('id')
)

# Average experience years
avg_experience = Doctor.objects.aggregate(Avg('experience_years'))

# Maximum experience
max_experience = Doctor.objects.aggregate(Max('experience_years'))

# Count total doctors
total = Doctor.objects.aggregate(total=Count('id'))
```

**URLs:**
- List all: `/doctors/`
- Detail view: `/doctors/<id>/`

---

## Update Operations

### 1. Update Single Record

```python
# Get the doctor
doctor = Doctor.objects.get(pk=1)

# Update fields
doctor.first_name = 'Updated Name'
doctor.experience_years = 15
doctor.is_available = False
doctor.save()  # Saves changes to database
```

### 2. Update Using update() Method (Bulk Update)

```python
# Update multiple records at once (more efficient)
Doctor.objects.filter(specialization='general').update(
    is_available=False
)

# Update single record using update()
Doctor.objects.filter(pk=1).update(
    experience_years=20,
    is_available=True
)
```

### 3. Update with Conditions

```python
# Update all available cardiologists
Doctor.objects.filter(
    specialization='cardiology',
    is_available=True
).update(experience_years=15)

# Update using F() expressions (update based on existing value)
from django.db.models import F

# Increment experience_years by 1 for all doctors
Doctor.objects.all().update(experience_years=F('experience_years') + 1)
```

### 4. Update Using Django Forms (In Views)

```python
# In views.py
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save()  # ORM: Updates doctor record
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'myapp/doctor_form.html', {'form': form, 'doctor': doctor})
```

**URL:** `/doctors/<id>/edit/`

---

## Delete Operations

### 1. Delete Single Record

```python
# Get and delete
doctor = Doctor.objects.get(pk=1)
doctor.delete()  # Deletes from database

# Delete directly
Doctor.objects.get(pk=1).delete()
```

### 2. Delete Multiple Records

```python
# Delete all records matching condition
Doctor.objects.filter(specialization='general').delete()

# Delete all records (use with caution!)
Doctor.objects.all().delete()
```

### 3. Delete Using Django Views

```python
# In views.py
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        doctor_name = doctor.get_full_name()
        doctor.delete()  # ORM: Deletes doctor record
        messages.success(request, f'Doctor {doctor_name} deleted successfully!')
        return redirect('doctor-list')
    
    return render(request, 'myapp/doctor_confirm_delete.html', {'doctor': doctor})
```

**URL:** `/doctors/<id>/delete/`

---

## Advanced ORM Queries

### 1. Select Related (Optimize Foreign Key Queries)

```python
# If Doctor had foreign keys, use select_related
# appointments = Appointment.objects.select_related('doctor').all()
```

### 2. Prefetch Related (Optimize Many-to-Many/Reverse FK)

```python
# Get doctors with their appointments (optimized)
doctors = Doctor.objects.prefetch_related('appointments').all()
for doctor in doctors:
    appointments = doctor.appointments.all()  # No additional query
```

### 3. Values and Values List

```python
# Get specific fields as dictionaries
doctors_data = Doctor.objects.values('first_name', 'last_name', 'specialization')

# Get specific fields as tuples
doctors_tuples = Doctor.objects.values_list('first_name', 'last_name')

# Get flat list (single field)
doctor_names = Doctor.objects.values_list('first_name', flat=True)
```

### 4. Annotations

```python
from django.db.models import Count

# Annotate each doctor with appointment count
doctors_with_counts = Doctor.objects.annotate(
    appointment_count=Count('appointments')
)
```

### 5. Distinct

```python
# Get unique specializations
unique_specializations = Doctor.objects.values_list(
    'specialization', flat=True
).distinct()
```

### 6. Exists and Count

```python
# Check if any doctors exist
has_doctors = Doctor.objects.exists()

# Count with conditions
cardiology_count = Doctor.objects.filter(specialization='cardiology').count()
```

---

## Complete CRUD Example in Views

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Doctor
from .forms import DoctorForm

# CREATE
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()  # ORM CREATE
            messages.success(request, 'Doctor created!')
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})

# READ (List)
def doctor_list(request):
    doctors = Doctor.objects.all()  # ORM READ (all)
    return render(request, 'doctor_list.html', {'doctors': doctors})

# READ (Detail)
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)  # ORM READ (single)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

# UPDATE
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save()  # ORM UPDATE
            messages.success(request, 'Doctor updated!')
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_form.html', {'form': form})

# DELETE
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()  # ORM DELETE
        messages.success(request, 'Doctor deleted!')
        return redirect('doctor-list')
    return render(request, 'doctor_confirm_delete.html', {'doctor': doctor})
```

---

## URL Configuration

```python
from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor-list'),           # READ (List)
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor-detail'), # READ (Detail)
    path('doctors/new/', views.doctor_create, name='doctor-create'),    # CREATE
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor-update'), # UPDATE
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor-delete'), # DELETE
]
```

---

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

---

## Best Practices

1. **Use `get_or_create()`** to avoid duplicate entries
2. **Use `bulk_create()`** for inserting multiple records
3. **Use `update()`** for bulk updates instead of looping
4. **Use `select_related()` and `prefetch_related()`** to optimize queries
5. **Always use `get_object_or_404()`** in views instead of `get()`
6. **Use transactions** for multiple related operations
7. **Validate data** before saving using forms
8. **Use `exists()`** instead of `count() > 0` for boolean checks

---

## Summary

| Operation | ORM Method | Example |
|-----------|-----------|---------|
| **Create** | `objects.create()` | `Doctor.objects.create(...)` |
| **Read (All)** | `objects.all()` | `Doctor.objects.all()` |
| **Read (Single)** | `objects.get()` | `Doctor.objects.get(pk=1)` |
| **Read (Filter)** | `objects.filter()` | `Doctor.objects.filter(specialization='cardiology')` |
| **Update** | `save()` or `update()` | `doctor.save()` or `Doctor.objects.filter(...).update(...)` |
| **Delete** | `delete()` | `doctor.delete()` or `Doctor.objects.filter(...).delete()` |

---

**Last Updated:** 2024  
**Django Version:** 5.2.8

