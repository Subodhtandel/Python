from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Specialty(models.Model):
    """Medical specialties"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🏥')  # Emoji icon

    class Meta:
        verbose_name_plural = "Specialties"
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Doctor model"""
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)

    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialties = models.ManyToManyField(Specialty, related_name='doctors')
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        default=0
    )
    qualification = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    # Availability
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )
    working_hours_start = models.TimeField(default='09:00')
    working_hours_end = models.TimeField(default='17:00')

    # Location
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=10, blank=True)

    # Pricing
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Rating
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'first_name']
        indexes = [
            models.Index(fields=['city', 'availability_status']),
            models.Index(fields=['-rating']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_specialties_display(self):
        return ", ".join([s.name for s in self.specialties.all()])


class Appointment(models.Model):
    """Appointment model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Patient Information
    patient_name = models.CharField(max_length=200)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    patient_age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    
    # Appointment Details
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    
    # Medical Information
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Payment Information
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['order_id']),
        ]

    def __str__(self):
        return f"Appointment {self.order_id} - {self.patient_name} with {self.doctor.get_full_name()}"


