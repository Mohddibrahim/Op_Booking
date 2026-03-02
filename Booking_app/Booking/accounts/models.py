from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES=(
        ('SUPERADMIN','Super admin'),
        ('FACILITYADMIN','Facility admin'),
        ('DOCTOR','Doctor'),
        ('PATIENT','Patient'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')

    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

