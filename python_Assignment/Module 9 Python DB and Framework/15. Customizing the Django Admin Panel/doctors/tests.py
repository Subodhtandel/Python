from django.test import TestCase
from .models import Doctor, Specialty, AvailabilitySchedule


class DoctorModelTest(TestCase):
    """Test cases for Doctor model"""

    def setUp(self):
        """Set up test data"""
        self.specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            license_number="DOC123456",
            experience_years=10,
            availability_status="available",
            consultation_fee=150.00,
            rating=4.5
        )
        self.doctor.specialties.add(self.specialty)

    def test_doctor_str(self):
        """Test doctor string representation"""
        self.assertEqual(str(self.doctor), "Dr. John Doe")

    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.doctor.get_full_name(), "John Doe")

    def test_get_specialties_display(self):
        """Test get_specialties_display method"""
        self.assertIn("Cardiology", self.doctor.get_specialties_display())

    def test_get_experience_level(self):
        """Test get_experience_level method"""
        self.assertEqual(self.doctor.get_experience_level(), "Experienced")

    def test_doctor_creation(self):
        """Test doctor creation"""
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(self.doctor.email, "john.doe@example.com")


class SpecialtyModelTest(TestCase):
    """Test cases for Specialty model"""

    def test_specialty_str(self):
        """Test specialty string representation"""
        specialty = Specialty.objects.create(name="Neurology")
        self.assertEqual(str(specialty), "Neurology")

    def test_specialty_ordering(self):
        """Test specialty ordering"""
        Specialty.objects.create(name="Zebra")
        Specialty.objects.create(name="Alpha")
        specialties = list(Specialty.objects.all())
        self.assertEqual(specialties[0].name, "Alpha")


class AvailabilityScheduleTest(TestCase):
    """Test cases for AvailabilitySchedule model"""

    def setUp(self):
        """Set up test data"""
        self.specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            license_number="DOC123456"
        )
        self.doctor.specialties.add(self.specialty)

    def test_schedule_creation(self):
        """Test schedule creation"""
        schedule = AvailabilitySchedule.objects.create(
            doctor=self.doctor,
            day="monday",
            start_time="09:00",
            end_time="17:00",
            is_available=True
        )
        self.assertEqual(AvailabilitySchedule.objects.count(), 1)
        self.assertEqual(schedule.doctor, self.doctor)


