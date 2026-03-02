from django.db import transaction, IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from facilities.models import MedicalFacility
from doctors.models import Doctor
from appointments.models import Appointment, TimeSlot
from payment.models import Payment


# --------------------------
# Public pages
# --------------------------
def home(request):
    hospitals = MedicalFacility.objects.filter(status='APPROVED', facility_type='HOSPITAL')
    clinics = MedicalFacility.objects.filter(status='APPROVED', facility_type='CLINIC')
    return render(request, 'home.html', {'hospitals': hospitals, 'clinics': clinics})


def about_view(request):
    return render(request, 'about.html')


def confirm_view(request):
    return render(request, 'confirm.html')


def hospitals_list(request):
    hospitals = MedicalFacility.objects.filter(status='APPROVED', facility_type='HOSPITAL')
    return render(request, 'hospitals_list.html', {'hospitals': hospitals})


def clinics_list(request):
    clinics = MedicalFacility.objects.filter(status='APPROVED', facility_type='CLINIC')
    return render(request, 'clinics_list.html', {'clinics': clinics})


def hospital_doctors(request, hospital_id):
    doctors = Doctor.objects.filter(facility_id=hospital_id)
    return render(request, 'doctor_list.html', {'doctors': doctors})


def clinic_doctors(request, clinic_id):
    doctors = Doctor.objects.filter(facility_id=clinic_id, status='APPROVED', is_blocked=False)
    return render(request, 'doctor_list.html', {'doctors': doctors})


# --------------------------
# Doctor slots & confirmation
# --------------------------
def doctor_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, status='APPROVED', is_blocked=False)
    
    # Only show slots that are not booked
    slots = TimeSlot.objects.filter(doctor=doctor, is_booked=False).order_by('date', 'start_time')

    return render(request, 'slot_list.html', {
        'slots': slots,
        'doctor': doctor
    })




@login_required
def confirm_slot(request, slot_id):
    """
    Show confirmation page for a slot if it is still available.
    """
    try:
        slot = TimeSlot.objects.select_related('doctor').get(id=slot_id)
    except TimeSlot.DoesNotExist:
        messages.error(request, "This slot does not exist.")
        return redirect('home')

    if slot.is_booked or Appointment.objects.filter(slot=slot, status='confirmed').exists():
        messages.error(request, "Sorry, this slot is no longer available.")
        return redirect('doctor_slots', doctor_id=slot.doctor.id)

    return render(request, 'confirm_slot.html', {'slot': slot})


# --------------------------
# Booking & Payment
# --------------------------
@login_required
def book_appointment(request, slot_id):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect('home')

    patient_name = request.POST.get('patient_name', '').strip()
    if not patient_name:
        messages.error(request, "Please enter patient's name.")
        return redirect('confirm_slot', slot_id=slot_id)

    try:
        with transaction.atomic():

            slot = TimeSlot.objects.select_for_update().get(id=slot_id)

            if slot.is_booked:
                messages.error(request, "Sorry, this slot has just been booked.")
                return redirect('doctor_slots', doctor_id=slot.doctor.id)

            # 🔥 ALWAYS CREATE NEW APPOINTMENT
            booking = Appointment.objects.create(
                user=request.user,
                doctor=slot.doctor,
                slot=slot,
                patient_name=patient_name,
                status='pending'
            )

    except (TimeSlot.DoesNotExist, IntegrityError):
        messages.error(request, "This slot is not available.")
        return redirect('doctor_slots', doctor_id=slot.doctor.id)

    return redirect('payment_page', booking_id=booking.id)




@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Appointment, id=booking_id)
    return render(request, 'payment.html', {'booking': booking})


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Appointment, id=booking_id)

    if Payment.objects.filter(booking=booking).exists():
        messages.info(request, "Payment already completed.")
        return redirect('my_appointments')

    # Confirm appointment and mark slot as booked
    booking.status = 'confirmed'
    booking.save()
    slot = booking.slot
    slot.is_booked = True
    slot.save()

    Payment.objects.create(
        booking=booking,
        amount=slot.price,
        transaction_id=f"TXN{booking.id}{timezone.now().strftime('%f')}",
        is_paid=True
    )

    messages.success(request, "Payment successful! Appointment confirmed.")
    return redirect('my_appointments')


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).select_related('doctor', 'slot').order_by('-created_at')
    return render(request, 'my_appointments.html', {'appointments': appointments})


@login_required
def cancel_user_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    # Only allow cancellation if appointment has a free slot (or simply always allow cancellation)
    if appointment.status != "confirmed":
        messages.error(request, "Cannot cancel this appointment.")
        return redirect('my_appointments')

    appointment.status = 'cancelled'
    appointment.save()

    # Free the slot
    slot = appointment.slot
    slot.is_booked = False
    slot.save()

    messages.success(request, "Appointment cancelled successfully.")
    return redirect('my_appointments')


@login_required
def show_reschedule_slots(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    doctor = appointment.doctor

    # Only show slots that are free
    available_slots = TimeSlot.objects.filter(doctor=doctor, is_booked=False).exclude(id=appointment.slot.id).order_by('date', 'start_time')

    if not available_slots.exists():
        messages.error(request, "No available slots to reschedule.")
        return redirect('my_appointments')

    return render(request, 'reschedule_slots.html', {
        'appointment': appointment,
        'available_slots': available_slots
    })


@login_required
def reschedule(request, appointment_id, new_slot_id):
    

    try:
        with transaction.atomic():

            booking = Appointment.objects.select_for_update().get(
                id=appointment_id,
                user=request.user
            )

            new_slot = TimeSlot.objects.select_for_update().get(
                id=new_slot_id
            )

            # Prevent double booking
            if new_slot.is_booked:
                messages.error(request, "Selected slot is already booked.")
                return redirect('show_reschedule_slots',
                                appointment_id=booking.id)

            # Free old slot
            old_slot = booking.slot
            old_slot.is_booked = False
            old_slot.save()

            # Assign new slot
            booking.slot = new_slot
            booking.status = 'confirmed'
            booking.save()

            new_slot.is_booked = True
            new_slot.save()

            messages.success(request,
                             "Appointment rescheduled successfully.")
            return redirect('my_appointments')

    except Exception:
        messages.error(request, "Reschedule failed.")
        return redirect('my_appointments')