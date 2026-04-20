from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from django.db.models import Q
from .models import Flight, Booking
from .forms import FlightForm

def home(request):
    flights = Flight.objects.filter(departure_date__gte=timezone.now().date()).order_by('departure_date', 'departure_time')
    context = {
        'title': 'Home',
        'page': 'home',
        'flights': flights
    }
    return render(request, 'base/home.html', context)

def about(request):
    context = {
        'title': 'About',
        'page': 'about'
    }
    return render(request, 'base/about.html', context)

def booking(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to book a flight.')
        return redirect('base:login')
    
    if request.method == 'POST':
        try:
            passenger_name = request.POST.get('passenger_name')
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            adhar_no = request.POST.get('adhar_no')
            age = request.POST.get('age')
            seat_class = request.POST.get('seat_class')
            seat_no = request.POST.get('seat_no')
            flight_id = request.POST.get('flight_id')
            
            # Validation
            if not all([passenger_name, email, phone_no, adhar_no, age, seat_class, seat_no, flight_id]):
                messages.error(request, '✗ All fields are required.')
                return redirect('base:booking')
            
            if len(phone_no) != 10 or not phone_no.isdigit():
                messages.error(request, '✗ Invalid phone number. Must be 10 digits.')
                return redirect('base:booking')
            
            if len(adhar_no) != 12 or not adhar_no.isdigit():
                messages.error(request, '✗ Invalid Aadhar number. Must be 12 digits.')
                return redirect('base:booking')
            
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    messages.error(request, '✗ Invalid age. Must be between 1 and 120.')
                    return redirect('base:booking')
            except:
                messages.error(request, '✗ Age must be a valid number.')
                return redirect('base:booking')
            
            flight = Flight.objects.get(id=flight_id)
            
            # Check if seat is already booked
            if Booking.objects.filter(flight=flight, seat_no=seat_no).exists():
                messages.error(request, f'✗ Seat {seat_no} is already booked. Please select another seat.')
                return redirect('base:booking')
            
            booking_obj = Booking.objects.create(
                flight=flight,
                passenger_name=passenger_name,
                email=email,
                phone_no=phone_no,
                adhar_no=adhar_no,
                age=age,
                seat_class=seat_class,
                seat_no=seat_no,
                flight_company=flight.flight_company,
                flight_name=flight.flight_name,
                flight_no=flight.flight_no,
                from_city=flight.from_city,
                to_city=flight.to_city,
                departure_date=flight.departure_date,
                departure_time=flight.departure_time,
                price=flight.price,
                status='confirmed'
            )
            messages.success(request, f'✓ Booking confirmed! Booking ID: #{booking_obj.id}')
            return redirect('base:history')
        except Flight.DoesNotExist:
            messages.error(request, '✗ Flight not found.')
        except Exception as e:
            messages.error(request, f'✗ Error: {str(e)}')
    
    flights = Flight.objects.filter(departure_date__gte=timezone.now().date()).order_by('departure_date', 'departure_time')
    context = {
        'title': 'Book Flight',
        'page': 'booking',
        'flights': flights
    }
    return render(request, 'base/booking.html', context)

def booking_history(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view booking history.')
        return redirect('base:login')
    
    # Show all bookings (can be filtered by user email if they want)
    bookings = Booking.objects.all().order_by('-booking_date')
    context = {
        'title': 'Booking History',
        'page': 'history',
        'bookings': bookings
    }
    return render(request, 'base/booking_history.html', context)

def support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # You can save this to a model or send an email
        messages.success(request, f'✓ Thank you, {name}! Your message has been received. We will contact you soon.')
        return redirect('base:support')
    
    context = {
        'title': 'Support',
        'page': 'support'
    }
    return render(request, 'base/support.html', context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view your profile.')
        return redirect('base:home')
    
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Check if email is already in use by another user
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, '✗ Email already in use by another account.')
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, '✓ Profile updated successfully!')
            return redirect('base:profile')
    
    context = {
        'title': 'Profile',
        'page': 'profile',
        'user': request.user
    }
    return render(request, 'base/profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, '✓ You have been logged out successfully.')
    return redirect('base:home')

def change_password(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to change your password.')
        return redirect('base:home')
    
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not user.check_password(old_password):
            messages.error(request, '✗ Old password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, '✗ New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, '✗ Password must be at least 8 characters long.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, '✓ Password changed successfully. Please login again.')
            logout(request)
            return redirect('base:home')
    
    context = {
        'title': 'Change Password',
        'page': 'profile'
    }
    return render(request, 'base/change_password.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✓ Welcome back, {username}!')
            return redirect('base:home')
        else:
            messages.error(request, '✗ Invalid username or password.')
    
    context = {
        'title': 'Login',
        'page': 'login'
    }
    return render(request, 'base/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists. Please choose a different one.')
        
        if not email or '@' not in email:
            errors.append('Invalid email address.')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered. Please use a different email.')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, f'✗ {error}')
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, '✓ Account created successfully! Please login.')
            return redirect('base:login')
    
    context = {
        'title': 'Register',
        'page': 'register'
    }
    return render(request, 'base/register.html', context)

def add_flight(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access this page.')
        return redirect('base:login')
    
    if not request.user.is_staff:
        messages.error(request, '✗ You do not have permission to add flights.')
        return redirect('base:home')
    
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save()
            messages.success(request, f'✓ Flight {flight.flight_no} added successfully!')
            return redirect('base:add-flight')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'✗ {field}: {error}')
    else:
        form = FlightForm()
    
    flights = Flight.objects.all().order_by('-created_at')
    
    context = {
        'title': 'Add Flight',
        'page': 'admin',
        'form': form,
        'flights': flights
    }
    return render(request, 'base/add_flight.html', context)

def edit_flight(request, flight_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access this page.')
        return redirect('base:login')
    
    if not request.user.is_staff:
        messages.error(request, '✗ You do not have permission to edit flights.')
        return redirect('base:home')
    
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, f'✓ Flight {flight.flight_no} updated successfully!')
            return redirect('base:add-flight')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'✗ {field}: {error}')
    else:
        form = FlightForm(instance=flight)
    
    context = {
        'title': 'Edit Flight',
        'page': 'admin',
        'form': form,
        'flight': flight,
        'is_edit': True
    }
    return render(request, 'base/edit_flight.html', context)

def delete_flight(request, flight_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access this page.')
        return redirect('base:login')
    
    if not request.user.is_staff:
        messages.error(request, '✗ You do not have permission to delete flights.')
        return redirect('base:home')
    
    flight = get_object_or_404(Flight, id=flight_id)
    flight_no = flight.flight_no
    flight.delete()
    messages.success(request, f'✓ Flight {flight_no} deleted successfully!')
    return redirect('base:add-flight')
