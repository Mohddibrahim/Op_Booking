from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor
from .forms import DoctorForm
from appointments.models import Appointment
from facilities.models import MedicalFacility

from django.utils import timezone
from django.db.models import Sum
from datetime import date

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.db.models import Sum
from datetime import date

from .models import Doctor
from .forms import DoctorForm
from appointments.models import Appointment, TimeSlot
from facilities.models import MedicalFacility
from payment.models import Payment

# --------------------------
# Doctor Dashboard & Profile
# --------------------------
@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        return redirect('home')

    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('create_doctor_profile')

    if doctor.status != "APPROVED" or doctor.is_blocked:
        return render(request, "dashboards/doctor_waiting.html", {"doctor": doctor})

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related('slot', 'user')

    # Counters
    total_appointments = appointments.count()
    today_appointments = appointments.filter(
    slot__date=date.today(),
    status="confirmed"
    ).count()

    cancelled_appointments = appointments.filter(
        status="cancelled"
    ).count()

    completed_appointments = appointments.filter(
        status="completed"
    ).count()

    total_earnings = appointments.filter(
        status__in=["confirmed", "completed"]
    ).aggregate(
        total=Sum('slot__price')
    )['total'] or 0

    upcoming = appointments.filter(
        slot__date__gte=date.today(),
        status="confirmed"
    ).order_by('slot__date', 'slot__start_time')

    past = appointments.filter(
        slot__date__lt=date.today(),
        status__in=["confirmed", "completed"]
    ).order_by('-slot__date')
    profile_fields = [doctor.name, doctor.specialization, doctor.facility]
    completed = sum(bool(field) for field in profile_fields)
    profile_completion = int((completed / len(profile_fields)) * 100)

    return render(request, 'dashboards/doctor.html', {
        'doctor': doctor,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'cancelled_appointments': cancelled_appointments,
        'completed_appointments': completed_appointments,
        'total_earnings': total_earnings,
        'upcoming': upcoming,
        'past': past,
        'profile_completion': profile_completion,
    })


@login_required
def mark_completed(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    if doctor.status != "APPROVED" or doctor.is_blocked:
        return redirect('doctor_dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    appointment.status = "completed"
    appointment.save()
    messages.success(request, "Appointment marked as completed.")
    return redirect('doctor_dashboard')


@login_required
def create_doctor_profile(request):
    if Doctor.objects.filter(user=request.user).exists():
        return redirect('doctor_dashboard')

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user
            doctor.save()
            messages.success(request, "Profile created successfully.")
            return redirect('doctor_dashboard')
    else:
        form = DoctorForm()

    return render(request, 'dashboards/create_doctor.html', {'form': form})


@login_required
def update_doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('doctor_dashboard')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'dashboards/create_doctor.html', {'form': form})



@login_required
def cancel_appointment(request, id):
    messages.error(request, "Doctors cannot cancel appointments.")
    return redirect('doctor_dashboard')

