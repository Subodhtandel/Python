from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    salary = models.FloatField()
    age = models.IntegerField()
    image=models.ImageField(upload_to="profile_pic")