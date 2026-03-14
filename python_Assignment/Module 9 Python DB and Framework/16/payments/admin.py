from django.contrib import admin
from .models import PaytmTransaction


@admin.register(PaytmTransaction)
class PaytmTransactionAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'transaction_id', 'appointment', 'amount', 'status', 'bank_name', 'created_at']
    list_filter = ['status', 'created_at', 'bank_name']
    search_fields = ['order_id', 'transaction_id', 'bank_transaction_id', 'appointment__patient_name']
    readonly_fields = ['created_at', 'updated_at', 'transaction_date']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('order_id', 'transaction_id', 'appointment', 'amount', 'status')
        }),
        ('Bank Details', {
            'fields': ('bank_transaction_id', 'bank_name', 'gateway_name')
        }),
        ('Paytm Response', {
            'fields': ('response_code', 'response_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'transaction_date'),
            'classes': ('collapse',)
        }),
    )


