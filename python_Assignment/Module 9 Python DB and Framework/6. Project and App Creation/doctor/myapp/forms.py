from django import forms
from .models import Doctor, Appointment, Patient


class DoctorForm(forms.ModelForm):
    """
    Form for creating and updating Doctor records
    """
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'phone', 
                  'specialization', 'license_number', 'experience_years', 'is_available']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'specialization': forms.Select(attrs={
                'class': 'form-control'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter license number'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter years of experience'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AppointmentForm(forms.ModelForm):
    """
    Form for creating and updating Appointment records
    """
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient_name', 'patient_email', 
                  'appointment_date', 'reason', 'status', 'notes']
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient name'
            }),
            'patient_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient email'
            }),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reason for appointment',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes',
                'rows': 3
            }),
        }


class PatientRegistrationForm(forms.ModelForm):
    """
    Patient registration form with email and phone validation
    """
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'id': 'id_first_name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'id': 'id_last_name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address (e.g., user@example.com)',
                'id': 'id_email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number (e.g., +1234567890 or 123-456-7890)',
                'id': 'id_phone'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_date_of_birth'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3,
                'id': 'id_address'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Additional server-side email validation
            if not email or '@' not in email:
                raise forms.ValidationError("Please enter a valid email address.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common phone number formatting characters
            cleaned_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            # Check if phone contains only digits (after removing formatting)
            if not cleaned_phone.isdigit():
                raise forms.ValidationError("Phone number should contain only digits and common formatting characters.")
            if len(cleaned_phone) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone
