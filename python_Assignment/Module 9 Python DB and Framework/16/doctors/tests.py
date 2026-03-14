from django.test import TestCase
from .models import Doctor, Specialty, Appointment


class DoctorModelTest(TestCase):
    """Test cases for Doctor model"""

    def setUp(self):
        self.specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            license_number="DOC001",
            consultation_fee=500.00
        )
        self.doctor.specialties.add(self.specialty)

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "Dr. John Doe")

    def test_get_full_name(self):
        self.assertEqual(self.doctor.get_full_name(), "John Doe")


class AppointmentModelTest(TestCase):
    """Test cases for Appointment model"""

    def setUp(self):
        self.specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            license_number="DOC001",
            consultation_fee=500.00
        )
        self.doctor.specialties.add(self.specialty)

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            patient_name="Jane Smith",
            patient_email="jane@example.com",
            patient_phone="9876543210",
            patient_age=30,
            doctor=self.doctor,
            amount=500.00,
            order_id="ORD123456"
        )
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(appointment.patient_name, "Jane Smith")


