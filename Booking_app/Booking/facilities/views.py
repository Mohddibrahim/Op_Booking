from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import MedicalFacility
from .forms import FacilityForm
from doctors.models  import Doctor
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.


@login_required
def create_facility(request):

    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES)

        if form.is_valid():
            facility = form.save(commit=False)
            facility.admin = request.user   # VERY IMPORTANT
            facility.save()
            return redirect('facility_dashboard')
        else:
            print(form.errors)  
    else:
        form = FacilityForm()

    return render(request, 'dashboards/create_facility.html', {'form': form})

@login_required
def facility_dashboard(request):
    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    facilities = MedicalFacility.objects.filter(admin=request.user)
    doctors = Doctor.objects.filter(facility__in=facilities)

    return render(
        request,
        'dashboards/facility.html',
        {'facilities': facilities,
          'doctors':doctors}
    )



@login_required
def facility_doctors(request):
    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    facility = MedicalFacility.objects.get(admin=request.user)
    doctors = facility.doctors.all()

    return render(request,'dashboards/doctors.html',{
        'doctors': doctors
    })
    
@login_required
def approve_doctor(request, doctor_id):

    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Ensure doctor belongs to this facility admin
    if doctor.facility.admin != request.user:
        return redirect('facility_dashboard')

    doctor.status = "APPROVED"
    doctor.save()

    messages.success(request, "Doctor approved successfully.")
    return redirect('facility_dashboard')

@login_required
def reject_doctor(request, doctor_id):

    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if doctor.facility.admin != request.user:
        return redirect('facility_dashboard')

    doctor.status = "REJECTED"
    doctor.save()

    messages.warning(request, "Doctor rejected.")
    return redirect('facility_dashboard')

    
@login_required
def toggle_block_doctor(request, doctor_id):

    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if doctor.facility.admin != request.user:
        return redirect('facility_dashboard')

    doctor.is_blocked = not doctor.is_blocked
    doctor.save()

    return redirect('facility_dashboard')
@login_required
def doctor_detail(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if doctor.facility.admin != request.user:
        return redirect('facility_dashboard')

    return render(request, 'dashboards/doctor_detail.html', {
        'doctor': doctor
    })

@login_required
def update_facility(request, facility_id):

    facility = get_object_or_404(
        MedicalFacility,
        id=facility_id,
        admin=request.user
    )

    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES, instance=facility)

        if form.is_valid():
            form.save()
            messages.success(request, "Facility updated successfully.")
            return redirect('facility_dashboard')
    else:
        form = FacilityForm(instance=facility)

    return render(request, 'dashboards/update_facility.html', {
        'form': form,
        'facility': facility
    })