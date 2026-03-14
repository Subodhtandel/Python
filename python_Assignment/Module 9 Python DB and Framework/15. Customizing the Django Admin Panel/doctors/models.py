from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Specialty(models.Model):
    """Model to store medical specialties"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Specialties"
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Doctor model with comprehensive information"""
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave'),
        ('unavailable', 'Unavailable'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)

    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialties = models.ManyToManyField(Specialty, related_name='doctors', blank=False)
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        default=0
    )
    qualification = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    # Availability Information
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )
    working_hours_start = models.TimeField(default='09:00')
    working_hours_end = models.TimeField(default='17:00')
    is_active = models.BooleanField(default=True)

    # Contact Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='USA')

    # Additional Information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    total_appointments = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        indexes = [
            models.Index(fields=['availability_status', 'is_active']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the doctor's full name"""
        return f"{self.first_name} {self.last_name}"

    def get_specialties_display(self):
        """Return comma-separated list of specialties"""
        return ", ".join([s.name for s in self.specialties.all()])

    def get_availability_badge_color(self):
        """Return badge color class for availability status"""
        colors = {
            'available': 'green',
            'busy': 'orange',
            'on_leave': 'blue',
            'unavailable': 'red',
        }
        return colors.get(self.availability_status, 'gray')

    def get_experience_level(self):
        """Return experience level based on years"""
        if self.experience_years >= 20:
            return "Senior"
        elif self.experience_years >= 10:
            return "Experienced"
        elif self.experience_years >= 5:
            return "Mid-level"
        else:
            return "Junior"

    def is_available_now(self):
        """Check if doctor is currently available"""
        if not self.is_active or self.availability_status != 'available':
            return False
        now = timezone.now().time()
        return self.working_hours_start <= now <= self.working_hours_end


class AvailabilitySchedule(models.Model):
    """Model to store doctor's weekly availability schedule"""
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['doctor', 'day']
        ordering = ['doctor', 'day']

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.get_day_display()}"


