"""
Django management command to demonstrate CRUD operations on Doctor model
Run with: python manage.py demo_crud
"""
from django.core.management.base import BaseCommand
from myapp.models import Doctor


class Command(BaseCommand):
    help = 'Demonstrates CRUD operations on Doctor profiles using Django ORM'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Django ORM CRUD Operations Demo ===\n'))
        
        # Clean up any existing demo data first
        Doctor.objects.filter(license_number__startswith='DEMO').delete()
        self.stdout.write('[INFO] Cleaned up any existing demo data\n')
        
        # CREATE Operations
        self.stdout.write(self.style.WARNING('1. CREATE OPERATIONS'))
        self.stdout.write('-' * 50)
        
        # Create single doctor
        doctor1 = Doctor.objects.create(
            first_name='John',
            last_name='Smith',
            email='john.smith@demo.com',
            phone='123-456-7890',
            specialization='cardiology',
            license_number='DEMO001',
            experience_years=10,
            is_available=True
        )
        self.stdout.write(f'[OK] Created: {doctor1}')
        
        # Create another doctor
        doctor2 = Doctor.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@demo.com',
            phone='987-654-3210',
            specialization='dermatology',
            license_number='DEMO002',
            experience_years=5,
            is_available=True
        )
        self.stdout.write(f'[OK] Created: {doctor2}')
        
        # READ Operations
        self.stdout.write(self.style.WARNING('\n2. READ OPERATIONS'))
        self.stdout.write('-' * 50)
        
        # Read all
        all_doctors = Doctor.objects.all()
        self.stdout.write(f'[OK] Total doctors: {all_doctors.count()}')
        
        # Read single
        doctor = Doctor.objects.get(pk=doctor1.pk)
        self.stdout.write(f'[OK] Retrieved doctor: {doctor}')
        
        # Filter
        cardiologists = Doctor.objects.filter(specialization='cardiology')
        self.stdout.write(f'[OK] Cardiologists found: {cardiologists.count()}')
        
        # READ Operations
        self.stdout.write(self.style.WARNING('\n3. UPDATE OPERATIONS'))
        self.stdout.write('-' * 50)
        
        # Update single field
        doctor1.experience_years = 15
        doctor1.save()
        self.stdout.write(f'[OK] Updated experience: {doctor1.experience_years} years')
        
        # Bulk update
        updated = Doctor.objects.filter(specialization='cardiology').update(is_available=False)
        self.stdout.write(f'[OK] Bulk updated {updated} cardiologist(s)')
        
        # DELETE Operations
        self.stdout.write(self.style.WARNING('\n4. DELETE OPERATIONS'))
        self.stdout.write('-' * 50)
        
        # Delete single
        doctor_name = doctor2.get_full_name()
        doctor2.delete()
        self.stdout.write(f'[OK] Deleted: {doctor_name}')
        
        # Clean up demo data
        Doctor.objects.filter(license_number__startswith='DEMO').delete()
        self.stdout.write('[OK] Cleaned up demo data')
        
        self.stdout.write(self.style.SUCCESS('\n=== CRUD Demo Complete ===\n'))
        self.stdout.write('All CRUD operations demonstrated successfully!')
        self.stdout.write('Check the CRUD_OPERATIONS.md file for detailed documentation.')

