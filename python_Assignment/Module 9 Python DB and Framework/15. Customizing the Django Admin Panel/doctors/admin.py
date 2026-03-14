from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Doctor, Specialty, AvailabilitySchedule


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    """Admin interface for Specialty model"""
    list_display = ['name', 'doctor_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

    def doctor_count(self, obj):
        """Display count of doctors with this specialty"""
        count = obj.doctors.count()
        url = reverse('admin:doctors_doctor_changelist')
        return format_html(
            '<a href="{}?specialties__id__exact={}">{}</a>',
            url,
            obj.pk,
            count
        )
    doctor_count.short_description = 'Number of Doctors'


class AvailabilityScheduleInline(admin.TabularInline):
    """Inline admin for AvailabilitySchedule"""
    model = AvailabilitySchedule
    extra = 7  # One for each day of the week
    fields = ['day', 'start_time', 'end_time', 'is_available']
    ordering = ['day']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Customized Admin interface for Doctor model with detailed information"""

    # List Display - What columns to show in the list view
    list_display = [
        'doctor_photo',
        'full_name_with_title',
        'specialties_list',
        'availability_status_badge',
        'experience_info',
        'consultation_fee_display',
        'rating_display',
        'is_active',
        'created_at'
    ]

    # List filters - Filter options on the right sidebar
    list_filter = [
        'availability_status',
        'is_active',
        'specialties',
        'city',
        'state',
        'experience_years',
        'created_at',
    ]

    # Search fields - What fields to search in
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'license_number',
        'specialties__name',
        'city',
        'state',
    ]

    # Readonly fields - Fields that cannot be edited
    readonly_fields = [
        'created_at',
        'updated_at',
        'doctor_photo_preview',
        'experience_level_display',
        'availability_info',
    ]

    # Fieldsets - Organize fields into sections
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'doctor_photo_preview',
                'profile_picture',
                ('first_name', 'last_name'),
                ('email', 'phone'),
                'date_of_birth',
            ),
            'classes': ('wide',)
        }),
        ('Professional Information', {
            'fields': (
                'license_number',
                'specialties',
                'qualification',
                ('experience_years', 'experience_level_display'),
                'bio',
            ),
        }),
        ('Availability & Schedule', {
            'fields': (
                'availability_status',
                'availability_info',
                ('working_hours_start', 'working_hours_end'),
                'is_active',
            ),
        }),
        ('Contact Information', {
            'fields': (
                'address',
                ('city', 'state', 'zip_code'),
                'country',
            ),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': (
                'consultation_fee',
                ('rating', 'total_appointments'),
            ),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Inline editing
    inlines = [AvailabilityScheduleInline]

    # Actions - Bulk actions
    actions = ['make_available', 'make_unavailable', 'activate_doctors', 'deactivate_doctors']

    # Pagination
    list_per_page = 25

    # Date hierarchy - Filter by date at the top
    date_hierarchy = 'created_at'

    # Ordering
    ordering = ['-created_at']

    # Custom methods for list display
    def doctor_photo(self, obj):
        """Display doctor photo thumbnail in list view"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return format_html('<div style="width: 50px; height: 50px; background: #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px;">👨‍⚕️</div>')
    doctor_photo.short_description = 'Photo'

    def full_name_with_title(self, obj):
        """Display full name with clickable link"""
        url = reverse('admin:doctors_doctor_change', args=[obj.pk])
        return format_html(
            '<a href="{}"><strong>Dr. {} {}</strong></a><br><small>{}</small>',
            url,
            obj.first_name,
            obj.last_name,
            obj.email
        )
    full_name_with_title.short_description = 'Doctor Name'
    full_name_with_title.admin_order_field = 'last_name'

    def specialties_list(self, obj):
        """Display specialties as badges"""
        specialties = obj.specialties.all()
        if specialties:
            badges = []
            for specialty in specialties:
                color = '#007bff'  # Blue color
                badges.append(
                    format_html(
                        '<span style="background-color: {}; color: white; padding: 3px 8px; '
                        'border-radius: 3px; font-size: 11px; margin-right: 3px; display: inline-block;">{}</span>',
                        color,
                        specialty.name
                    )
                )
            return format_html(''.join(badges))
        return format_html('<span style="color: #999;">No specialties</span>')
    specialties_list.short_description = 'Specialties'

    def availability_status_badge(self, obj):
        """Display availability status with colored badge"""
        colors = {
            'available': '#28a745',  # Green
            'busy': '#ffc107',       # Yellow/Orange
            'on_leave': '#17a2b8',   # Blue
            'unavailable': '#dc3545', # Red
        }
        color = colors.get(obj.availability_status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; '
            'border-radius: 15px; font-size: 11px; font-weight: bold; text-transform: uppercase;">{}</span>',
            color,
            obj.get_availability_status_display()
        )
    availability_status_badge.short_description = 'Availability'
    availability_status_badge.admin_order_field = 'availability_status'

    def experience_info(self, obj):
        """Display experience with level"""
        level = obj.get_experience_level()
        return format_html(
            '<strong>{} years</strong><br><small style="color: #666;">{}</small>',
            obj.experience_years,
            level
        )
    experience_info.short_description = 'Experience'
    experience_info.admin_order_field = 'experience_years'

    def consultation_fee_display(self, obj):
        """Display consultation fee formatted"""
        return format_html('<strong>${:.2f}</strong>', obj.consultation_fee)
    consultation_fee_display.short_description = 'Fee'
    consultation_fee_display.admin_order_field = 'consultation_fee'

    def rating_display(self, obj):
        """Display rating with stars"""
        stars = '★' * int(obj.rating)
        half_star = '☆' if obj.rating % 1 >= 0.5 else ''
        empty_stars = '☆' * (5 - int(obj.rating) - (1 if half_star else 0))
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}{}{}</span> '
            '<strong>{:.2f}</strong>',
            stars,
            half_star,
            empty_stars,
            obj.rating
        )
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'

    # Custom methods for detail view
    def doctor_photo_preview(self, obj):
        """Display doctor photo in detail view"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 10px; object-fit: cover; border: 3px solid #007bff;" />',
                obj.profile_picture.url
            )
        return format_html('<div style="width: 200px; height: 200px; background: #ddd; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 60px;">👨‍⚕️</div>')
    doctor_photo_preview.short_description = 'Profile Picture'

    def experience_level_display(self, obj):
        """Display experience level"""
        level = obj.get_experience_level()
        colors = {
            'Senior': '#28a745',
            'Experienced': '#007bff',
            'Mid-level': '#ffc107',
            'Junior': '#6c757d',
        }
        color = colors.get(level, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            color,
            level
        )
    experience_level_display.short_description = 'Level'

    def availability_info(self, obj):
        """Display detailed availability information"""
        available_now = obj.is_available_now()
        status_color = '#28a745' if available_now else '#dc3545'
        status_text = 'Currently Available' if available_now else 'Currently Unavailable'
        
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid {};">'
            '<strong>Status:</strong> {}<br>'
            '<strong>Working Hours:</strong> {} - {}<br>'
            '<strong>Active:</strong> {}'
            '</div>',
            status_color,
            status_text,
            obj.working_hours_start.strftime('%I:%M %p'),
            obj.working_hours_end.strftime('%I:%M %p'),
            'Yes' if obj.is_active else 'No'
        )
    availability_info.short_description = 'Availability Details'

    # Admin actions
    def make_available(self, request, queryset):
        """Bulk action: Make selected doctors available"""
        updated = queryset.update(availability_status='available', is_active=True)
        self.message_user(request, f'{updated} doctor(s) marked as available.')
    make_available.short_description = 'Mark selected doctors as available'

    def make_unavailable(self, request, queryset):
        """Bulk action: Make selected doctors unavailable"""
        updated = queryset.update(availability_status='unavailable')
        self.message_user(request, f'{updated} doctor(s) marked as unavailable.')
    make_unavailable.short_description = 'Mark selected doctors as unavailable'

    def activate_doctors(self, request, queryset):
        """Bulk action: Activate selected doctors"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} doctor(s) activated.')
    activate_doctors.short_description = 'Activate selected doctors'

    def deactivate_doctors(self, request, queryset):
        """Bulk action: Deactivate selected doctors"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} doctor(s) deactivated.')
    deactivate_doctors.short_description = 'Deactivate selected doctors'


@admin.register(AvailabilitySchedule)
class AvailabilityScheduleAdmin(admin.ModelAdmin):
    """Admin interface for AvailabilitySchedule"""
    list_display = ['doctor', 'day', 'start_time', 'end_time', 'is_available']
    list_filter = ['day', 'is_available', 'doctor']
    search_fields = ['doctor__first_name', 'doctor__last_name']
    ordering = ['doctor', 'day']


