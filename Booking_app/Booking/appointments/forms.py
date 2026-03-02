from django import forms
from .models import TimeSlot
from django.utils import timezone




class TimeSlotForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    interval = forms.IntegerField(
        initial=15,
        help_text="Enter interval in minutes (e.g. 15)"
    )
    price = forms.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("date")
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        if date and date < timezone.now().date():
            raise forms.ValidationError("Cannot create slots in the past.")

        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned