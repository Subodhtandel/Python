from django.test import TestCase
from doctors.models import Doctor, Specialty, Appointment
from .models import PaytmTransaction
from .paytm_checksum import generate_checksum, verify_checksum


class PaytmChecksumTest(TestCase):
    """Test cases for Paytm checksum functions"""

    def setUp(self):
        self.merchant_key = "test_merchant_key"
        self.test_params = {
            'MID': 'test_mid',
            'ORDER_ID': 'ORDER123',
            'TXN_AMOUNT': '100.00',
        }

    def test_generate_checksum(self):
        checksum = generate_checksum(self.test_params, self.merchant_key)
        self.assertIsNotNone(checksum)
        self.assertEqual(len(checksum), 64)  # SHA256 produces 64 character hex string

    def test_verify_checksum(self):
        checksum = generate_checksum(self.test_params, self.merchant_key)
        is_valid = verify_checksum(self.test_params, self.merchant_key, checksum)
        self.assertTrue(is_valid)

    def test_verify_checksum_invalid(self):
        checksum = generate_checksum(self.test_params, self.merchant_key)
        is_valid = verify_checksum(self.test_params, 'wrong_key', checksum)
        self.assertFalse(is_valid)


class PaytmTransactionTest(TestCase):
    """Test cases for PaytmTransaction model"""

    def setUp(self):
        specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            license_number="DOC001",
            consultation_fee=500.00
        )
        self.doctor.specialties.add(specialty)
        
        self.appointment = Appointment.objects.create(
            patient_name="Jane Smith",
            patient_email="jane@example.com",
            patient_phone="9876543210",
            patient_age=30,
            doctor=self.doctor,
            amount=500.00,
            order_id="ORD123456"
        )

    def test_transaction_creation(self):
        transaction = PaytmTransaction.objects.create(
            order_id="ORD123456",
            appointment=self.appointment,
            amount=500.00,
            status='pending'
        )
        self.assertEqual(PaytmTransaction.objects.count(), 1)
        self.assertEqual(transaction.status, 'pending')


