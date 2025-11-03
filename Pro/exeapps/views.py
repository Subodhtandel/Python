from django.shortcuts import render,redirect
from exeapps.models import *

# Create your views here.
def index(request):
    return render(request,"index.html")

def reg(request):
    if request.method=='POST':
        data = request.POST
        name = data.get('name')
        email =data.get('email')
        phone = data.get('phone')
        age = data.get('age')

        # print(name,email,phone,age)
        Student.objects.create(name=name, email=email, phone=phone, age=age)
        return render(request,'index.html',{"msg":"Registration Successfully"})
    

    return render(request, 'index.html')
def display(request):
    Students = Student.objects.all()
    return render(request,'display.html',{"students":Students})

# def delete_student(request):
#     request.GET['sid']
#     Student.objects.get(id=id)
#     Student.delete()
#     return redirect("display.html")
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("display")

def update_student(request, id):
    try:
        student = Student.objects.get(id=id)  
    except Student.DoesNotExist:
        return redirect('display')  

    if request.method == 'POST':
        data = request.POST
        student.name = data.get('name')
        student.email = data.get('email')
        student.phone = data.get('phone')
        student.age = data.get('age')
        student.save()  
        return redirect('display')

    return render(request, 'update.html', {'student': student})
