from django.shortcuts import render, HttpResponse
from ajexapp.models import Student, Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError 
from django.db.models import Q


def index(request):
    
    return render(request, "index.html")

# Register or update student
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = request.POST

        student_id = data.get('id')
        dept_id = data.get('dept') 
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')

        try:
            department_obj = Department.objects.get(id=dept_id) 
        except Department.DoesNotExist:
            return JsonResponse({"error": "Invalid department selected."}, status=400)

        try:
            if student_id:  
                try:
                    std = Student.objects.get(pk=student_id)
                except Student.DoesNotExist:
                    return JsonResponse({"error": "Student not found for update."}, status=404)
                
        
                if Student.objects.exclude(pk=student_id).filter(email=email).exists():
                     return JsonResponse({"error": "This email is already taken by another student."}, status=400)
                
                std.name = name
                std.department = department_obj 
                std.email = email
                std.phone = phone
                std.age = age
                std.save()
                return JsonResponse({"message": "Student record updated successfully!"})
            
            else: 
                Student.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    age=age,
                    department=department_obj 
                )
                return JsonResponse({"message": "New student registered successfully!"})
        
        except IntegrityError:
            return JsonResponse({"error": "Registration failed: A student with this email already exists."}, status=400)
        
        except Exception as e:
            print(f"Unexpected server error in register view: {e}") 
            return JsonResponse({"error": "An unexpected server error occurred during submission."}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)



def display(request):
    all_students = Student.objects.all().order_by('id')
    data = list(
        all_students.values(
            'id',
            'name',
            'email',
            'phone',
            'age',
            'department__id', 
            'department__name'
        )
    )
   
    
    return JsonResponse({"data": data})

def deptdisplay(request):
    
    all_depts = Department.objects.all()
    data = list(all_depts.values('id', 'name'))
    return JsonResponse({"data": data})

@csrf_exempt
def delete_std(request):
    student_id = request.GET.get('id')
    if not student_id:
        return JsonResponse({"error": "No student ID provided"}, status=400)
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return JsonResponse({"message": "Student deleted successfully!"})
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found for deletion."}, status=404)
    except Exception:
        return JsonResponse({"error": "An error occurred during deletion."}, status=500)



def databyid(request):
    student_id = request.GET.get('id')
    if not student_id:
        return JsonResponse({"error": "No student ID provided"}, status=400)
    try:
       
        
        student = Student.objects.filter(id=student_id)
        
        data = list(student.values('id', 'department_id', 'name', 'email', 'phone', 'age'))
        
        if not data:
             return JsonResponse({"error": "Student not found."}, status=404)
             
        data[0]['dept_id'] = data[0].pop('department_id')

        return JsonResponse({"std": data})
    except Exception:
        return JsonResponse({"error": "An error occurred while fetching data."}, status=500)  
    

def search(request):
    value = request.GET.get('value')
    searchedStd = Student.objects.filter(Q(name__startswith=value) |Q(email__startswith=value)|Q(age__startswith=value))
    data = list(
        searchedStd.values(
            'id',
            'name',
            'email',
            'phone',
            'age',
            'department__id', 
            'department__name'
        )
    )
   
    
    return JsonResponse({"data": data})


def checkmail(request):
    email = request.GET['email']
    exists = Student.objects.filter(email=email).exists()
    return HttpResponse(exists)