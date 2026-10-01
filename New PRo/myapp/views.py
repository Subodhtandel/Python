import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .models import Member, Attendance

# Dashboard Page
def index_view(request):
    return render(request, 'index1.html')

# 1. Get All Members API (Public View)
def get_members(request):
    members = list(Member.objects.values('id', 'name', 'plan', 'avatar', 'join_date'))
    return JsonResponse(members, safe=False)

# 2. Get Attendance API (Public View)
def get_attendance(request, member_id, year_month):
    try:
        year, month = map(int, year_month.split('-'))
    except ValueError:
        return JsonResponse({'error': 'Invalid format'}, status=400)

    attendances = Attendance.objects.filter(
        member_id=member_id,
        date__year=year,
        date__month=month
    )
    attendance_map = {att.date.day: att.status for att in attendances}
    return JsonResponse(attendance_map)

# 3. Toggle Attendance API (Locked - Sirf Admin / Staff hi change kar sakta hai)
@csrf_exempt
def toggle_attendance(request):
    # Security Check: Agar user admin/staff nahi hai to reject kar do
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized! Sirf Admin attendance change kar sakta hai.'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        member_id = data.get('memberId')
        date_str = data.get('dateStr')
        status = data.get('status')

        if not member_id or not date_str or not status:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if status == 'off':
            Attendance.objects.filter(member_id=member_id, date=date_str).delete()
            return JsonResponse({'message': 'Attendance set to Off'})
        else:
            Attendance.objects.update_or_create(
                member_id=member_id,
                date=date_str,
                defaults={'status': status}
            )
            return JsonResponse({'message': 'Attendance updated successfully', 'status': status})

    return JsonResponse({'error': 'Only POST method allowed'}, status=400)