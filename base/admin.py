from django.contrib import admin
from .models import Flight, Booking

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_no', 'flight_name', 'flight_company', 'from_city', 'to_city', 'departure_date', 'departure_time', 'price', 'available_seats')
    list_filter = ('flight_company', 'departure_date', 'from_city', 'to_city')
    search_fields = ('flight_no', 'flight_name', 'from_city', 'to_city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Flight Information', {
            'fields': ('flight_company', 'flight_name', 'flight_no')
        }),
        ('Route', {
            'fields': ('from_city', 'to_city')
        }),
        ('Timing & Pricing', {
            'fields': ('departure_date', 'departure_time', 'price')
        }),
        ('Capacity', {
            'fields': ('available_seats',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger_name', 'flight_no', 'from_city', 'to_city', 'seat_no', 'seat_class', 'status', 'booking_date')
    list_filter = ('status', 'seat_class', 'booking_date', 'departure_date')
    search_fields = ('passenger_name', 'email', 'phone_no', 'flight_no', 'adhar_no')
    readonly_fields = ('booking_date', 'flight_company', 'flight_name', 'flight_no', 'from_city', 'to_city', 'departure_time', 'departure_date', 'price')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('flight', 'status', 'booking_date')
        }),
        ('Flight Details', {
            'fields': ('flight_company', 'flight_name', 'flight_no', 'from_city', 'to_city', 'departure_date', 'departure_time', 'price')
        }),
        ('Passenger Information', {
            'fields': ('passenger_name', 'email', 'phone_no', 'adhar_no', 'age')
        }),
        ('Seat Information', {
            'fields': ('seat_class', 'seat_no')
        }),
    )
