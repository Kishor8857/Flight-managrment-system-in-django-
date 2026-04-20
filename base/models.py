from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class Flight(models.Model):
    SEAT_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_no = models.CharField(max_length=20, unique=True)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=180)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-departure_date', 'departure_time']
        verbose_name_plural = 'Flights'
    
    def __str__(self):
        return f"{self.flight_no} - {self.from_city} to {self.to_city}"


class Booking(models.Model):
    SEAT_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    
    # Flight Details (stored for record)
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_no = models.CharField(max_length=20)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Passenger Details
    passenger_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_no = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')]
    )
    adhar_no = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{12}$', 'Adhar number must be 12 digits')]
    )
    age = models.IntegerField()
    seat_class = models.CharField(max_length=50, choices=SEAT_CLASS_CHOICES)
    seat_no = models.CharField(max_length=10)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {self.id} - {self.passenger_name} - {self.flight_no}"
