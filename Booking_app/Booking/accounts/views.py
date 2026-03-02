from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import UserSignupForm,UserLoginForm
from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from facilities.models import MedicalFacility
from accounts.models import User
# Create your views here.

def signup_view(request):
    if request.method=="POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # PATIENT auto approved
            if user.role == 'PATIENT':
                user.is_approved = True
            else:
                user.is_approved = False   # needs admin approval

            user.save()

            # login only if approved
            if user.is_approved:
                login(request,user)
                return redirect('home')
            else:
                return render(request,'accounts/wait_approval.html')

    else:
        form = UserSignupForm()

    return render(request,'accounts/signup.html',{'form':form})




def login_view(request):
    if request.method=="POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.is_blocked:
                return render(request, 'accounts/blocked.html')

            if not user.is_approved:
                return render(request,'accounts/wait_approval.html')

            login(request,user)

            if user.role == 'SUPERADMIN':
                return redirect('superadmin_dashboard')
            elif user.role == 'FACILITYADMIN':
                return redirect('facility_dashboard')
            elif user.role == 'DOCTOR':
                return redirect('doctor_dashboard')
            else:
                return redirect('home')
    else:
        form = UserLoginForm()

    return render(request,'accounts/login.html',{'form':form})


        
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def superadmin_dashboard(request):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    facilities = MedicalFacility.objects.select_related('admin').all()
    facility_admins = User.objects.filter(role="FACILITYADMIN")

    return render(request, "dashboards/superadmin.html", {
        "facilities": facilities,
        "facility_admins": facility_admins,
    })


@login_required
def approve_facility(request, id):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    facility = get_object_or_404(MedicalFacility, id=id)
    facility.status = "APPROVED"
    facility.save()

    return redirect("superadmin_dashboard")


@login_required
def reject_facility(request, id):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    facility = get_object_or_404(MedicalFacility, id=id)
    facility.status = "REJECTED"
    facility.save()

    return redirect("superadmin_dashboard")


@login_required
def facility_detail(request, id):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    facility = get_object_or_404(MedicalFacility, id=id)

    return render(request, "dashboards/facility_detail.html", {
        "facility": facility
    })


@login_required
def block_facility_admin(request, id):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    admin = get_object_or_404(User, id=id)
    admin.is_blocked = True
    admin.save()

    return redirect("superadmin_dashboard")


@login_required
def unblock_facility_admin(request, id):
    if request.user.role != "SUPERADMIN":
        return redirect('home')

    admin = get_object_or_404(User, id=id)
    admin.is_blocked = False
    admin.save()

    return redirect("superadmin_dashboard")




@login_required
def facility_dashboard(request):
    if request.user.role != "FACILITYADMIN" or request.user.is_blocked:
        return redirect("login")

    doctors = User.objects.filter(role="DOCTOR")
    return render(request,'dashboards/facility.html', {
        "doctors": doctors
    })




@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR' or request.user.is_blocked:
        return redirect('login')

    return render(request,'dashboards/doctor.html')





@login_required
def approve_facility_admins(request):
    if request.user.role != 'SUPERADMIN':
        return redirect('home')

    pending_users = User.objects.filter(role='FACILITYADMIN', is_approved=False)

    return render(request, 'approvals/facility_admin_list.html', {
        'users': pending_users
    })
    
@login_required
def approve_user(request, user_id):
    if request.user.role not in ['SUPERADMIN','FACILITYADMIN']:
        return redirect('home')

    user = User.objects.get(id=user_id)
    user.is_approved = True
    user.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def approve_doctors(request):
    if request.user.role != 'FACILITYADMIN':
        return redirect('home')

    doctors = User.objects.filter(role='DOCTOR', is_approved=False)

    return render(request,'approvals/doctor_list.html',{
        'users': doctors
    })

@login_required
def block_user(request, user_id):
    if request.user.role != 'SUPERADMIN':
        return redirect('home')

    user = User.objects.get(id=user_id)

    # Prevent self block
    if user == request.user:
        return redirect('superadmin_dashboard')

    user.is_blocked = not user.is_blocked
    user.save()

    return redirect('superadmin_dashboard')
