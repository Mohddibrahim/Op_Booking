from django.shortcuts import render, redirect
from .models import TimeSlot
from .forms import TimeSlotForm
from doctors.models import Doctor
from django.contrib.auth.decorators import login_required



from datetime import datetime, timedelta
from appointments.models import TimeSlot

@login_required
def create_slot(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('create_doctor_profile')

    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            interval = form.cleaned_data['interval']
            price = form.cleaned_data['price']

            start_dt = datetime.combine(date, start_time)
            end_dt = datetime.combine(date, end_time)

            created = 0

            while start_dt + timedelta(minutes=interval) <= end_dt:
                slot_end = start_dt + timedelta(minutes=interval)

                # Prevent overlapping
                overlapping = TimeSlot.objects.filter(
                    doctor=doctor,
                    date=date,
                    start_time__lt=slot_end.time(),
                    end_time__gt=start_dt.time()
                ).exists()

                if not overlapping:
                    TimeSlot.objects.create(
                        doctor=doctor,
                        date=date,
                        start_time=start_dt.time(),
                        end_time=slot_end.time(),
                        price=price
                    )
                    created += 1

                start_dt = slot_end

            return redirect('doctor_dashboard')

    else:
        form = TimeSlotForm()

    return render(request, 'create_slot.html', {'form': form})