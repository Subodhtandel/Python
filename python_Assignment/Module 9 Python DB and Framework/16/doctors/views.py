from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Doctor, Specialty, Appointment
from .forms import AppointmentBookingForm, DoctorSearchForm
import uuid


def home(request):
    """Home page with doctor search"""
    form = DoctorSearchForm(request.GET or None)
    doctors = Doctor.objects.filter(availability_status='available')
    
    if form.is_valid():
        specialty_query = form.cleaned_data.get('specialty')
        city_query = form.cleaned_data.get('city')
        
        if specialty_query:
            doctors = doctors.filter(specialties__name__icontains=specialty_query)
        
        if city_query:
            doctors = doctors.filter(city__icontains=city_query)
    
    specialties = Specialty.objects.all()[:8]
    
    context = {
        'form': form,
        'doctors': doctors[:12],  # Limit to 12 doctors
        'specialties': specialties,
    }
    return render(request, 'doctors/home.html', context)


def doctor_list(request):
    """List all available doctors"""
    form = DoctorSearchForm(request.GET or None)
    doctors = Doctor.objects.filter(availability_status='available')
    
    if form.is_valid():
        specialty_query = form.cleaned_data.get('specialty')
        city_query = form.cleaned_data.get('city')
        
        if specialty_query:
            doctors = doctors.filter(specialties__name__icontains=specialty_query)
        
        if city_query:
            doctors = doctors.filter(city__icontains=city_query)
    
    context = {
        'form': form,
        'doctors': doctors,
    }
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, doctor_id):
    """Doctor detail page with booking form"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.amount = doctor.consultation_fee
            appointment.order_id = f"ORD{uuid.uuid4().hex[:12].upper()}"
            appointment.save()
            
            # Redirect to payment page
            return redirect('initiate_payment', appointment_id=appointment.id)
    else:
        form = AppointmentBookingForm()
    
    context = {
        'doctor': doctor,
        'form': form,
    }
    return render(request, 'doctors/doctor_detail.html', context)


def appointment_confirmation(request, appointment_id):
    """Display appointment confirmation after successful payment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctors/appointment_confirmation.html', context)


