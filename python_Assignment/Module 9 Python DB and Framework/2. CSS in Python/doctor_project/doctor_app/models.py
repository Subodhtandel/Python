from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    bio = models.TextField()
    rating = models.FloatField(default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
