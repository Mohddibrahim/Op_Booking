from django.urls import path
from .views import* 

urlpatterns = [
path('signup/', signup_view, name='signup'),
path('login/', login_view, name='login'),
path('logout/', logout_view, name='logout'),
path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),
path('facility/dashboard/', facility_dashboard, name='facility_dashboard'),
path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
path('approve/facility-admins/', approve_facility_admins, name='approve_facility_admins'),
path('approve/doctors/',approve_doctors, name='approve_doctors'),
path('approve/user/<int:user_id>/', approve_user, name='approve_user'),
path('block/user/<int:user_id>/', block_user, name='block_user'),



 path('facility/<int:id>/', facility_detail, name='facility_detail'),
    path('approve/<int:id>/', approve_facility, name='approve_facility'),
    path('reject/<int:id>/', reject_facility, name='reject_facility'),
    path('block-admin/<int:id>/', block_facility_admin, name='block_facility_admin'),
    path('unblock-admin/<int:id>/', unblock_facility_admin, name='unblock_facility_admin'),



]