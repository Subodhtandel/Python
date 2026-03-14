from django.db import models
from doctors.models import Appointment


class PaytmTransaction(models.Model):
    """Model to store Paytm payment transactions"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Payment Information
    order_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Paytm Response
    response_code = models.CharField(max_length=10, blank=True, null=True)
    response_message = models.TextField(blank=True, null=True)
    gateway_name = models.CharField(max_length=50, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment {self.order_id} - {self.status}"


