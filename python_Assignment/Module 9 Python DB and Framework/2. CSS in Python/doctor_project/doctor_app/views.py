from django.shortcuts import render
from .models import Doctor


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})


def doctor_detail(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    return render(request, 'doctor/doctor_detail.html', {'doctor': doctor})
