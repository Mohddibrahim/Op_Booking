from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create/', views.create_doctor_profile, name='create_doctor_profile'),
    path('cancel_appointment/<int:id>/',views.cancel_appointment,name='cancel_appointment'),
    path('update/', views.update_doctor_profile, name='update_doctor_profile'),
    path('appointment/<int:appointment_id>/complete/', 
     views.mark_completed, 
     name='mark_completed'),


    
]
