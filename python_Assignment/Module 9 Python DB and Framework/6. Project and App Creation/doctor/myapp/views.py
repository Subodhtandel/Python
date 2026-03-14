from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Doctor, Appointment, Patient
from .forms import DoctorForm, AppointmentForm, PatientRegistrationForm


# ==================== Function-Based Views ====================

def home(request):
    """
    Home page view showing welcome message and statistics
    """
    total_doctors = Doctor.objects.count()
    available_doctors = Doctor.objects.filter(is_available=True).count()
    total_appointments = Appointment.objects.count()
    
    context = {
        'total_doctors': total_doctors,
        'available_doctors': available_doctors,
        'total_appointments': total_appointments,
    }
    return render(request, 'myapp/home.html', context)


def doctor_list(request):
    """
    READ Operation - Display list of all doctors with filtering options
    Demonstrates Django ORM: .all(), .filter()
    """
    # ORM: Get all doctor records from database
    doctors = Doctor.objects.all()
    
    # ORM: Filter by specialization (if provided)
    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    # ORM: Filter by availability status
    availability = request.GET.get('availability')
    if availability == 'available':
        doctors = doctors.filter(is_available=True)
    elif availability == 'unavailable':
        doctors = doctors.filter(is_available=False)
    
    # Get unique specializations for filter dropdown
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'doctors': doctors,
        'specializations': specializations,
        'selected_specialization': specialization,
    }
    return render(request, 'myapp/doctor_list.html', context)


def doctor_detail(request, pk):
    """
    READ Operation - Display detailed information about a specific doctor
    Demonstrates Django ORM: get_object_or_404(), related object access
    """
    # ORM: Get single doctor record by primary key (returns 404 if not found)
    doctor = get_object_or_404(Doctor, pk=pk)
    # ORM: Access related appointments through ForeignKey relationship
    appointments = doctor.appointments.all()[:5]  # Get last 5 appointments
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
    }
    return render(request, 'myapp/doctor_detail.html', context)


def doctor_create(request):
    """
    CREATE Operation - Create a new doctor record
    Demonstrates Django ORM: form.save() which calls Model.save()
    """
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            # ORM: Create and save new doctor record to database
            # form.save() internally calls: Doctor.objects.create(...)
            doctor = form.save()
            messages.success(request, f'Doctor {doctor.get_full_name()} created successfully!')
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    
    return render(request, 'myapp/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})


def doctor_update(request, pk):
    """
    UPDATE Operation - Update an existing doctor record
    Demonstrates Django ORM: get_object_or_404(), form.save() with instance
    """
    # ORM: Get existing doctor record
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            # ORM: Update existing doctor record in database
            # form.save() internally calls: doctor.save() which updates the record
            doctor = form.save()
            messages.success(request, f'Doctor {doctor.get_full_name()} updated successfully!')
            return redirect('doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'myapp/doctor_form.html', {'form': form, 'title': 'Edit Doctor', 'doctor': doctor})


def doctor_delete(request, pk):
    """
    DELETE Operation - Delete a doctor record
    Demonstrates Django ORM: get_object_or_404(), Model.delete()
    """
    # ORM: Get existing doctor record
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        doctor_name = doctor.get_full_name()
        # ORM: Delete doctor record from database
        doctor.delete()
        messages.success(request, f'Doctor {doctor_name} deleted successfully!')
        return redirect('doctor-list')
    
    return render(request, 'myapp/doctor_confirm_delete.html', {'doctor': doctor})


def appointment_list(request):
    """
    Display list of all appointments
    """
    appointments = Appointment.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    # Filter by doctor
    doctor_id = request.GET.get('doctor')
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
    
    doctors = Doctor.objects.all()
    statuses = Appointment.STATUS_CHOICES
    
    context = {
        'appointments': appointments,
        'doctors': doctors,
        'statuses': statuses,
        'selected_status': status,
        'selected_doctor': doctor_id,
    }
    return render(request, 'myapp/appointment_list.html', context)


def appointment_detail(request, pk):
    """
    Display detailed information about an appointment
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'myapp/appointment_detail.html', context)


def appointment_create(request):
    """
    Create a new appointment
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('appointment-detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    
    return render(request, 'myapp/appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})


def appointment_update(request, pk):
    """
    Update an appointment
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment-detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'myapp/appointment_form.html', {'form': form, 'title': 'Edit Appointment', 'appointment': appointment})


def appointment_delete(request, pk):
    """
    Delete an appointment
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('appointment-list')
    
    return render(request, 'myapp/appointment_confirm_delete.html', {'appointment': appointment})


# ==================== API Views ====================

def api_doctors_json(request):
    """
    API endpoint to get all doctors as JSON
    """
    doctors = Doctor.objects.values('id', 'first_name', 'last_name', 'specialization', 'is_available')
    return JsonResponse(list(doctors), safe=False)


def api_doctor_detail_json(request, pk):
    """
    API endpoint to get a specific doctor as JSON
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    data = {
        'id': doctor.id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'email': doctor.email,
        'phone': doctor.phone,
        'specialization': doctor.specialization,
        'experience_years': doctor.experience_years,
        'is_available': doctor.is_available,
    }
    return JsonResponse(data)


def statistics(request):
    """
    Display statistics about doctors and appointments
    """
    total_doctors = Doctor.objects.count()
    available_doctors = Doctor.objects.filter(is_available=True).count()
    total_appointments = Appointment.objects.count()
    
    # Doctors by specialization
    specialization_stats = {}
    for spec_code, spec_name in Doctor.SPECIALIZATION_CHOICES:
        count = Doctor.objects.filter(specialization=spec_code).count()
        specialization_stats[spec_name] = count
    
    # Appointments by status
    status_stats = {}
    for status_code, status_name in Appointment.STATUS_CHOICES:
        count = Appointment.objects.filter(status=status_code).count()
        status_stats[status_name] = count
    
    context = {
        'total_doctors': total_doctors,
        'available_doctors': available_doctors,
        'unavailable_doctors': total_doctors - available_doctors,
        'total_appointments': total_appointments,
        'specialization_stats': specialization_stats,
        'status_stats': status_stats,
    }
    return render(request, 'myapp/statistics.html', context)


def patient_register(request):
    """
    Patient registration view with JavaScript validation
    """
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Registration successful! Welcome, {patient.get_full_name()}!')
            return redirect('registration-success', pk=patient.pk)
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'myapp/patient_register.html', {'form': form})


def registration_success(request, pk):
    """
    Display success message after registration
    """
    patient = get_object_or_404(Patient, pk=pk)
    context = {
        'patient': patient,
    }
    return render(request, 'myapp/registration_success.html', context)


# ==================== Doctor Finder Views ====================

def finder_home(request):
    """
    Doctor Finder home page
    """
    # Get featured doctors (available doctors)
    featured_doctors = Doctor.objects.filter(is_available=True)[:6]
    total_doctors = Doctor.objects.count()
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'featured_doctors': featured_doctors,
        'total_doctors': total_doctors,
        'specializations': specializations,
    }
    return render(request, 'myapp/finder_home.html', context)


def finder_profile(request, pk=None):
    """
    Doctor Finder profile page - shows individual doctor profile or list
    """
    if pk:
        # Show specific doctor profile
        doctor = get_object_or_404(Doctor, pk=pk)
        appointments = doctor.appointments.filter(status='scheduled')[:5]
        context = {
            'doctor': doctor,
            'appointments': appointments,
        }
        return render(request, 'myapp/finder_profile_detail.html', context)
    else:
        # Show all doctor profiles
        doctors = Doctor.objects.filter(is_available=True)
        
        # Filter by specialization
        specialization = request.GET.get('specialization')
        if specialization:
            doctors = doctors.filter(specialization=specialization)
        
        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            from django.db.models import Q
            doctors = doctors.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(specialization__icontains=search_query)
            )
        
        specializations = Doctor.SPECIALIZATION_CHOICES
        
        context = {
            'doctors': doctors,
            'specializations': specializations,
            'selected_specialization': specialization,
            'search_query': search_query,
        }
        return render(request, 'myapp/finder_profile.html', context)


def finder_contact(request):
    """
    Doctor Finder contact page
    """
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In a real application, you would send an email here
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('finder-contact')
    
    # Get contact information
    total_doctors = Doctor.objects.count()
    context = {
        'total_doctors': total_doctors,
    }
    return render(request, 'myapp/finder_contact.html', context)


# ==================== Database Management Views ====================

def database_info(request):
    """
    Display database connection information and statistics
    """
    from django.db import connection
    from django.conf import settings
    
    # Get database configuration
    db_config = settings.DATABASES['default']
    db_engine = db_config.get('ENGINE', '')
    db_name = db_config.get('NAME', '')
    
    # Determine database type
    if 'sqlite' in db_engine.lower():
        db_type = 'SQLite'
        db_path = str(db_name) if hasattr(db_name, '__str__') else db_name
    elif 'mysql' in db_engine.lower():
        db_type = 'MySQL'
        db_path = f"{db_config.get('HOST', 'localhost')}:{db_config.get('PORT', '3306')}"
    elif 'postgresql' in db_engine.lower():
        db_type = 'PostgreSQL'
        db_path = f"{db_config.get('HOST', 'localhost')}:{db_config.get('PORT', '5432')}"
    else:
        db_type = 'Unknown'
        db_path = 'N/A'
    
    # Test database connection
    connection_status = 'Connected'
    connection_error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        connection_status = 'Error'
        connection_error = str(e)
    
    # Get database statistics
    total_doctors = Doctor.objects.count()
    available_doctors = Doctor.objects.filter(is_available=True).count()
    total_appointments = Appointment.objects.count()
    total_patients = Patient.objects.count()
    
    # Get doctors by specialization
    specialization_stats = {}
    for code, name in Doctor.SPECIALIZATION_CHOICES:
        count = Doctor.objects.filter(specialization=code).count()
        if count > 0:
            specialization_stats[name] = count
    
    # Get recent database activity
    recent_doctors = Doctor.objects.order_by('-created_at')[:5]
    
    context = {
        'db_type': db_type,
        'db_engine': db_engine,
        'db_name': db_name if isinstance(db_name, str) else str(db_name),
        'db_path': db_path,
        'db_host': db_config.get('HOST', 'N/A'),
        'db_port': db_config.get('PORT', 'N/A'),
        'db_user': db_config.get('USER', 'N/A'),
        'connection_status': connection_status,
        'connection_error': connection_error,
        'total_doctors': total_doctors,
        'available_doctors': available_doctors,
        'total_appointments': total_appointments,
        'total_patients': total_patients,
        'specialization_stats': specialization_stats,
        'recent_doctors': recent_doctors,
    }
    return render(request, 'myapp/database_info.html', context)
