from django.urls import path
from .views import *

urlpatterns = [
    # Booking & Appointment
    path('book/<int:slot_id>/', book_appointment, name='book_appointment'),
    path('my-appointments/', my_appointments, name='my_appointments'),
    path('cancel-appointment/<int:appointment_id>/',
     cancel_user_appointment,
     name='cancel_user_appointment'),


path('reschedule/<int:appointment_id>/<int:new_slot_id>/', reschedule, name='reschedule_appointment'),

path('reschedule/<int:appointment_id>/', show_reschedule_slots, name='show_reschedule_slots'),





    # Payment
    path('payment/<int:booking_id>/', payment_page, name='payment_page'),
    path('payment/success/<int:booking_id>/', payment_success, name='payment_success'),

    # Other pages
    path('', home, name='home'),
    path('about/', about_view, name='about'),
    path('confirm/', confirm_view, name='confirm'),
    path('hospitals/', hospitals_list, name='hospitals_list'),
    path('clinics/', clinics_list, name='clinics_list'),
    path('hospital/<int:hospital_id>/doctors/', hospital_doctors, name='hospital_doctors'),
    path('clinic/<int:clinic_id>/doctors/', clinic_doctors, name='clinic_doctors'),
    path('doctor/<int:doctor_id>/slots/', doctor_slots, name='doctor_slots'),
    
    
    
    # slots & booking

path('confirm-slot/<int:slot_id>/', confirm_slot, name='confirm_slot'),

]
