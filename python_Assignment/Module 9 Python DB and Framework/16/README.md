# Doctor Finder - Django Project with Paytm Payment Integration

A comprehensive Django web application for finding and booking appointments with doctors, integrated with Paytm payment gateway for secure online payments.

## Features

### Doctor Management
- **Doctor Profiles**: Detailed doctor profiles with specialties, experience, ratings, and availability
- **Search & Filter**: Search doctors by specialty and city
- **Specialty Management**: Multiple medical specialties (Cardiology, Neurology, etc.)
- **Availability Tracking**: Real-time availability status and working hours

### Appointment Booking
- **Online Booking**: Easy appointment booking form
- **Patient Information**: Collect patient details (name, email, phone, age)
- **Appointment Scheduling**: Select date and time for appointments
- **Medical Notes**: Add symptoms and notes

### Paytm Payment Integration
- **Secure Payments**: Integrated Paytm payment gateway
- **Payment Processing**: Complete payment flow with checksum verification
- **Transaction Tracking**: Store and track all payment transactions
- **Payment Status**: Real-time payment status updates
- **Callback Handling**: Secure callback handling for payment verification

## Project Structure

```
16/
├── doctor_finder_project/     # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Django settings with Paytm configuration
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── doctors/                    # Doctors app
│   ├── __init__.py
│   ├── admin.py               # Admin interface
│   ├── apps.py
│   ├── models.py              # Doctor, Specialty, Appointment models
│   ├── forms.py               # Appointment booking form
│   ├── views.py               # Doctor views
│   ├── urls.py                # Doctor URLs
│   └── migrations/
├── payments/                   # Payments app
│   ├── __init__.py
│   ├── admin.py               # Payment admin
│   ├── apps.py
│   ├── models.py              # PaytmTransaction model
│   ├── views.py               # Payment views
│   ├── urls.py                # Payment URLs
│   └── paytm_checksum.py      # Checksum generation/verification
├── templates/                  # HTML templates
│   ├── base.html
│   ├── doctors/
│   │   ├── home.html
│   │   ├── doctor_list.html
│   │   ├── doctor_detail.html
│   │   └── appointment_confirmation.html
│   └── payments/
│       └── paytm_payment.html
├── static/                     # Static files (CSS, JS, images)
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Navigate to the project directory:
```bash
cd "Module 9 Python DB and Framework/16"
```

### 2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

### 3. Activate the virtual environment:
- On Windows (PowerShell):
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- On Windows (Command Prompt):
  ```bash
  venv\Scripts\activate.bat
  ```

### 4. Install dependencies:
```bash
pip install -r requirements.txt
```

### 5. Configure Paytm Credentials:

**IMPORTANT**: Before running the project, you need to configure Paytm credentials.

1. Sign up at [Paytm Business Dashboard](https://business.paytm.com/)
2. Get your Merchant ID (MID) and Merchant Key
3. Open `doctor_finder_project/settings.py`
4. Update the following settings:

```python
PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
PAYTM_WEBSITE = 'WEBSTAGING'  # Use 'WEBSTAGING' for testing
PAYTM_CALLBACK_URL = 'http://127.0.0.1:8000/payments/paytm-callback/'
```

**Note**: 
- For testing, use Paytm's staging environment with test credentials
- For production, change `PAYTM_WEBSITE` to `'DEFAULT'` and use production URLs

### 6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

### 8. Create sample data (optional):

You can create sample data using Django shell:

```bash
python manage.py shell
```

```python
from doctors.models import Specialty, Doctor

# Create specialties
specialties = ['Cardiology', 'Neurology', 'Dermatology', 'Orthopedics', 'Pediatrics', 'General Medicine']
for spec_name in specialties:
    Specialty.objects.get_or_create(name=spec_name)

# Create a sample doctor
cardiology = Specialty.objects.get(name='Cardiology')
doctor = Doctor.objects.create(
    first_name='John',
    last_name='Smith',
    email='john.smith@example.com',
    phone='1234567890',
    license_number='DOC001',
    experience_years=15,
    city='Mumbai',
    state='Maharashtra',
    consultation_fee=500.00,
    rating=4.5,
    availability_status='available'
)
doctor.specialties.add(cardiology)
```

### 9. Run the development server:
```bash
python manage.py runserver
```

### 10. Access the application:
- **Home**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## Usage

### For Patients:

1. **Browse Doctors**: Visit the home page to see available doctors
2. **Search Doctors**: Use the search form to filter by specialty or city
3. **View Doctor Details**: Click on a doctor to see full profile
4. **Book Appointment**: Fill the appointment booking form
5. **Make Payment**: Complete payment via Paytm
6. **Confirmation**: Receive appointment confirmation after successful payment

### For Administrators:

1. **Login to Admin**: http://127.0.0.1:8000/admin/
2. **Manage Doctors**: Add, edit, or remove doctors
3. **Manage Specialties**: Add medical specialties
4. **View Appointments**: Monitor all appointments
5. **View Payments**: Track payment transactions

## Paytm Integration Details

### Payment Flow:

1. **Initiate Payment**: When user books an appointment, payment is initiated
2. **Generate Checksum**: Server generates Paytm checksum using merchant key
3. **Redirect to Paytm**: User is redirected to Paytm payment gateway
4. **Payment Processing**: User completes payment on Paytm
5. **Callback Handling**: Paytm sends callback to our server
6. **Verify Checksum**: Server verifies the checksum
7. **Update Status**: Appointment and payment status are updated
8. **Confirmation**: User sees appointment confirmation

### Checksum Implementation:

The project includes a custom checksum implementation using HMAC SHA256. For production, it's recommended to use Paytm's official Python SDK:

```bash
pip install paytmchecksum
```

Then update `payments/paytm_checksum.py` to use the official SDK.

### Paytm URLs:

**Staging (Testing)**:
- Payment Gateway: `https://securegw-stage.paytm.in/order/process`
- Transaction Status: `https://securegw-stage.paytm.in/order/status`

**Production**:
- Payment Gateway: `https://securegw.paytm.in/order/process`
- Transaction Status: `https://securegw.paytm.in/order/status`

## Models

### Specialty
- Medical specialties (Cardiology, Neurology, etc.)

### Doctor
- Personal information (name, email, phone, profile picture)
- Professional information (license, specialties, experience, qualification)
- Availability (status, working hours)
- Location (address, city, state, zip)
- Pricing (consultation fee)
- Rating

### Appointment
- Patient information
- Doctor and appointment details
- Payment information (amount, order_id, payment_status)
- Appointment status

### PaytmTransaction
- Transaction details (order_id, transaction_id)
- Payment amount and status
- Bank details
- Paytm response data
- Timestamps

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never commit credentials**: Keep Paytm credentials in environment variables or secure config files
2. **Use HTTPS**: Always use HTTPS in production
3. **Verify Checksums**: Always verify Paytm checksums before processing payments
4. **Validate Amounts**: Double-check payment amounts match appointment fees
5. **Secure Callback**: Implement proper CSRF protection for callback endpoint
6. **Error Handling**: Handle payment failures gracefully
7. **Logging**: Log all payment transactions for audit

## Testing Paytm Integration

### Test Credentials:

For testing, use Paytm's test credentials from their staging environment:
- Use test Merchant ID and Key from Paytm Business Dashboard
- Test cards are available in Paytm's test documentation

### Test Payment Flow:

1. Create a test appointment
2. Proceed to payment
3. Use Paytm test credentials
4. Complete test payment
5. Verify callback handling
6. Check appointment confirmation

## Production Deployment

Before deploying to production:

1. ✅ Change `SECRET_KEY` in settings.py
2. ✅ Set `DEBUG = False`
3. ✅ Configure `ALLOWED_HOSTS`
4. ✅ Update Paytm credentials to production
5. ✅ Change `PAYTM_WEBSITE` to `'DEFAULT'`
6. ✅ Update Paytm URLs to production
7. ✅ Update `PAYTM_CALLBACK_URL` to production domain
8. ✅ Use HTTPS for all URLs
9. ✅ Configure proper database (PostgreSQL, MySQL)
10. ✅ Set up static files serving
11. ✅ Configure media files storage
12. ✅ Use environment variables for sensitive data
13. ✅ Implement proper logging
14. ✅ Set up monitoring and error tracking

## Technologies Used

- **Django 5.2.8**: Web framework
- **SQLite**: Database (development)
- **Pillow**: Image handling
- **Bootstrap 5**: Frontend framework
- **Paytm Payment Gateway**: Payment processing

## API Reference

### URLs:

- `/` - Home page
- `/doctors/` - Doctor list
- `/doctor/<id>/` - Doctor detail and booking
- `/payments/initiate/<appointment_id>/` - Initiate payment
- `/payments/paytm-callback/` - Paytm callback endpoint
- `/payments/status/<order_id>/` - Payment status
- `/appointment/<id>/confirmation/` - Appointment confirmation

## Troubleshooting

### Payment Issues:

1. **Checksum Mismatch**: Ensure merchant key is correct
2. **Callback Not Working**: Check callback URL is accessible
3. **Payment Failed**: Verify Paytm credentials and test mode settings
4. **Redirect Issues**: Ensure Paytm URLs are correct for staging/production

### Common Errors:

- **ModuleNotFoundError**: Install all requirements
- **Migration Errors**: Run `makemigrations` and `migrate`
- **Payment Gateway Error**: Check Paytm credentials and network connectivity

## License

This project is for educational purposes.

## Support

For Paytm integration support:
- Paytm Documentation: https://business.paytm.com/docs/
- Paytm Support: Contact through Paytm Business Dashboard

For Django support:
- Django Documentation: https://docs.djangoproject.com/


