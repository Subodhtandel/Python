from django.db import models

# Create your models here.
# class Student(models.Model):
#     Name=models.CharField(max_length=20)
#     Email=models.CharField(max_length=50)
#     Phone=models.CharField(max_length=20)
#     Age=models.IntegerField()

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
