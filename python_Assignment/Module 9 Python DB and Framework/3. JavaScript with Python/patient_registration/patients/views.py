from django.shortcuts import render, redirect
from .models import Patient
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        password = request.POST.get('password')
        # Basic server-side validation
        if not (first_name and last_name and email and phone and age and password):
            messages.error(request, 'All fields are required.')
            return redirect('register')
        # Save patient (note: password stored plain for demo only)
        Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=int(age),
            password=password,
        )
        return render(request, 'patients/success.html', {'first_name': first_name})
    return render(request, 'patients/register.html')
