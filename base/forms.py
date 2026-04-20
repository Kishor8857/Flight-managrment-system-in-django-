from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_company', 'flight_name', 'flight_no', 'from_city', 'to_city', 'departure_date', 'departure_time', 'price', 'available_seats']
        widgets = {
            'flight_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Emirates, Air India',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'flight_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Emirates Flight 1',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'flight_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., EK301',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'from_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dubai',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'to_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., India',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }, format='%Y-%m-%d'),
            'departure_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }, format='%H:%M'),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 10000.00',
                'step': '0.01',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'available_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 180',
                'min': '1',
                'style': 'padding: 10px; border: 1px solid #ddd; border-radius: 4px;'
            }),
        }
        labels = {
            'flight_company': 'Flight Company',
            'flight_name': 'Flight Name',
            'flight_no': 'Flight Number',
            'from_city': 'From City',
            'to_city': 'To City',
            'departure_date': 'Departure Date',
            'departure_time': 'Departure Time',
            'price': 'Price (₹)',
            'available_seats': 'Available Seats',
        }
