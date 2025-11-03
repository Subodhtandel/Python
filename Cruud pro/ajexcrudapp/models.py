from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=20)

    # def __str__(self):
    #     return  self.name
   

class Student(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()