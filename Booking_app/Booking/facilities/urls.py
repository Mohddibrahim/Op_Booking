from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.facility_dashboard, name='facility_dashboard'),
    path('create/', views.create_facility, name='create_facility'),
    path('doctor/<int:doctor_id>/approve/', views.approve_doctor, name='approve_doctor'),
path('doctor/<int:doctor_id>/reject/', views.reject_doctor, name='reject_doctor'),
path('doctor/<int:doctor_id>/block/', views.toggle_block_doctor, name='toggle_block_doctor'),
path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
path('update-facility/<int:facility_id>/',
     views.update_facility,
     name='update_facility'),

]
