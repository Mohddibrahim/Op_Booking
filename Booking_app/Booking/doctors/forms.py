from .models import Doctor
from django import forms

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name','facility','specialization','experience','image']

