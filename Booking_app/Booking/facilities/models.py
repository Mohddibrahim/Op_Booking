from django.db import models
from  django.conf import settings
# Create your models here.


class MedicalFacility(models.Model):
    TYPE_CHOICE=(
        ('HOSPITAL','Hospital'),
        ('CLINIC','Clinic')
    )
    
    name=models.CharField(max_length=50)
    facility_type=models.CharField(max_length=20,choices=TYPE_CHOICE)
    address = models.TextField()
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    image = models.ImageField(upload_to='facilities/', blank=True,null=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'), 
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name