import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import Flight
from datetime import datetime, timedelta

# Get today's date for future flights
today = datetime.now().date()

# Flight 1
Flight.objects.get_or_create(
    flight_no='301',
    defaults={
        'flight_company': 'Emirates',
        'flight_name': 'Emirates F1',
        'from_city': 'Dubai',
        'to_city': 'India',
        'departure_time': '15:30',
        'departure_date': today + timedelta(days=1),
        'price': 10000.00,
        'available_seats': 180
    }
)

# Flight 2
Flight.objects.get_or_create(
    flight_no='102',
    defaults={
        'flight_company': 'Indigo',
        'flight_name': 'Indigo A2',
        'from_city': 'Banglore',
        'to_city': 'Goa',
        'departure_time': '14:15',
        'departure_date': today + timedelta(days=2),
        'price': 7000.00,
        'available_seats': 180
    }
)

# Flight 3
Flight.objects.get_or_create(
    flight_no='201',
    defaults={
        'flight_company': 'Air India',
        'flight_name': 'Air India Express',
        'from_city': 'Mumbai',
        'to_city': 'Delhi',
        'departure_time': '10:00',
        'departure_date': today + timedelta(days=3),
        'price': 8500.00,
        'available_seats': 180
    }
)

print("✓ Flights added/updated successfully!")

# Flight 4
Flight.objects.get_or_create(
    flight_no='450',
    defaults={
        'flight_company': 'Spice Jet',
        'flight_name': 'Spice Jet Premium',
        'from_city': 'Chennai',
        'to_city': 'Hyderabad',
        'departure_time': '18:45',
        'departure_date': today + timedelta(days=1),
        'price': 6500.00,
        'available_seats': 180
    }
)

print("✅ All flights added/updated successfully!")
