from django.contrib import admin
from exeapps.models import*
# Register your models here.
class StudentModel(admin.ModelAdmin):
    list_display = ['id','name','email','phone','age']


admin.site.register(Student,StudentModel)