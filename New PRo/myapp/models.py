from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    avatar = models.URLField(default="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150")
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('off', 'Off'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('member', 'date')

    def __str__(self):
        return f"{self.member.name} - {self.date} - {self.status}"