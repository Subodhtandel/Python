from django.contrib import admin
from ajexcrudapp.models import *
# Register your models here.

class StudentModel(admin.ModelAdmin):
    list_display=['id','name','email','phone','age']

class DepartmentModel(admin.ModelAdmin):
    list_display=['id','name']

admin.site.register(Department,DepartmentModel)
admin.site.register(Student,StudentModel)