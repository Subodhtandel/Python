from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

class Company(models.Model):
    name=models.CharField(max_length=20,null=True)

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=20)
    price = models.FloatField()
    qty = models.IntegerField()