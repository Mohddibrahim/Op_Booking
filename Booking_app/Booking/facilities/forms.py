from django import forms
from .models import MedicalFacility

class FacilityForm(forms.ModelForm):
    class Meta:
        model = MedicalFacility
        fields = ['name', 'facility_type', 'address', 'city', 'image']
