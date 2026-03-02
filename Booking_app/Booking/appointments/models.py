from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    is_booked = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=400) 
    
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
    

    
    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time}"


class Appointment(models.Model):

    
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
   
    created_at = models.DateTimeField(auto_now_add=True)

    