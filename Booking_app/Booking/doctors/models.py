from django.db import models
from django.conf import settings
from facilities.models import MedicalFacility


class Doctor(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100, null=True, blank=True)

    facility = models.ForeignKey(
        MedicalFacility,
        on_delete=models.CASCADE,
        related_name='doctors'
    )

    specialization = models.CharField(max_length=200)
    experience = models.IntegerField()

    image = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )

    # 🔥 NEW FIELDS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.user.username
