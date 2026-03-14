import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from doctors.models import Appointment
from .models import PaytmTransaction
from .paytm_checksum import generate_checksum, verify_checksum


def initiate_payment(request, appointment_id):
    """Initiate Paytm payment for an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if payment already exists
    if hasattr(appointment, 'payment') and appointment.payment.status == 'success':
        messages.info(request, 'Payment already completed for this appointment.')
        return redirect('appointment_confirmation', appointment_id=appointment.id)
    
    # Create or get payment transaction
    payment, created = PaytmTransaction.objects.get_or_create(
        order_id=appointment.order_id,
        defaults={
            'appointment': appointment,
            'amount': appointment.amount,
            'status': 'pending'
        }
    )
    
    # Prepare Paytm parameters
    paytm_params = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': appointment.order_id,
        'TXN_AMOUNT': str(appointment.amount),
        'CUST_ID': appointment.patient_email,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
    }
    
    # Generate checksum
    checksum = generate_checksum(paytm_params, settings.PAYTM_MERCHANT_KEY)
    paytm_params['CHECKSUMHASH'] = checksum
    
    context = {
        'appointment': appointment,
        'paytm_params': paytm_params,
        'payment_gateway_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
    }
    
    return render(request, 'payments/paytm_payment.html', context)


@csrf_exempt
def paytm_callback(request):
    """Handle Paytm payment callback"""
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        
        # Extract checksum from received data
        paytm_checksum = received_data.get('CHECKSUMHASH', [None])[0]
        
        # Prepare parameters dictionary
        for key, value in received_data.items():
            if key != 'CHECKSUMHASH':
                paytm_params[key] = value[0] if isinstance(value, list) else value
        
        # Verify checksum
        is_valid_checksum = False
        if paytm_checksum:
            is_valid_checksum = verify_checksum(
                paytm_params,
                settings.PAYTM_MERCHANT_KEY,
                paytm_checksum
            )
        
        if is_valid_checksum:
            order_id = paytm_params.get('ORDERID')
            transaction_status = paytm_params.get('STATUS')
            
            try:
                payment = PaytmTransaction.objects.get(order_id=order_id)
                appointment = payment.appointment
                
                if transaction_status == 'TXN_SUCCESS':
                    # Payment successful
                    payment.status = 'success'
                    payment.transaction_id = paytm_params.get('TXNID')
                    payment.bank_transaction_id = paytm_params.get('BANKTXNID')
                    payment.bank_name = paytm_params.get('BANKNAME')
                    payment.response_code = paytm_params.get('RESPCODE')
                    payment.response_message = paytm_params.get('RESPMSG')
                    payment.gateway_name = paytm_params.get('GATEWAYNAME')
                    
                    # Update appointment
                    appointment.payment_status = 'completed'
                    appointment.status = 'confirmed'
                    appointment.save()
                    
                    payment.save()
                    
                    messages.success(request, 'Payment successful! Your appointment has been confirmed.')
                    return redirect('appointment_confirmation', appointment_id=appointment.id)
                    
                else:
                    # Payment failed
                    payment.status = 'failed'
                    payment.response_code = paytm_params.get('RESPCODE')
                    payment.response_message = paytm_params.get('RESPMSG')
                    payment.save()
                    
                    appointment.payment_status = 'failed'
                    appointment.save()
                    
                    messages.error(request, f'Payment failed: {paytm_params.get("RESPMSG", "Unknown error")}')
                    return redirect('doctor_detail', doctor_id=appointment.doctor.id)
                    
            except PaytmTransaction.DoesNotExist:
                messages.error(request, 'Payment transaction not found.')
                return redirect('home')
        else:
            messages.error(request, 'Checksum verification failed. Payment could not be processed.')
            return redirect('home')
    
    return redirect('home')


def payment_status(request, order_id):
    """Check payment status"""
    try:
        payment = PaytmTransaction.objects.get(order_id=order_id)
        context = {
            'payment': payment,
            'appointment': payment.appointment,
        }
        return render(request, 'payments/payment_status.html', context)
    except PaytmTransaction.DoesNotExist:
        messages.error(request, 'Payment not found.')
        return redirect('home')


