# forms.py
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'name', 'id_number', 'phone_number', 'address',
            'emergency_contact_name', 'emergency_contact_phone',
            'reservation_type', 'delivery_method', 'company_name',
            'company_email', 'company_contact'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].required = False
        self.fields['company_email'].required = False
        self.fields['company_contact'].required = False
