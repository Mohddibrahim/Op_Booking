from django.contrib import admin
# Register your models here.

from .models import TimeSlot, Appointment
admin.site.register(TimeSlot)
admin.site.register(Appointment)