from django.shortcuts import render,HttpResponse
from ajexcrudapp.models import *
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, "index.html")


def register(request):
    if request.method=='POST':
        data = request.POST

        id = data.get('id')
        dept_id = data.get('dept')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')
        dept = Department.objects.get(id=dept_id)

        if id : 
            std  =Student.objects.get(pk=id)
            std.name = name
            std.dept = dept
            std.email = email
            std.phone = phone
            std.age = age
            std.save()
            return HttpResponse("Update successfull Done !!!")
        else:
            Student.objects.create(name=name,email=email,phone=phone,age=age,dept=dept)
            return HttpResponse("Registration successfull Done !!!")
    
def display(request):
    allStudents = Student.objects.all()    
    
    data = list(
            allStudents.values(
                'id',
                'name',
                'email',
                'phone',
                'age',
                'dept__id',
                'dept__name', 
            )
        )
        
    return JsonResponse({"data": data})


def deptdisplay(request):
    alldetps = Department.objects.all()
    return JsonResponse({"data":list(alldetps.values())})

def delete_std(request):
    student = Student.objects.get(id = request.GET['id'])
    Student.delete(student)
    return HttpResponse("Student deleted !!!")

def databyid(request):
    student = Student.objects.filter(id = request.GET['id'])
    return JsonResponse({"std":list(student.values())})
     