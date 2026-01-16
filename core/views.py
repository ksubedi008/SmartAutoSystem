from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Location, Route, Booking

# IMPORTS FOR FORMS
from .forms import RegistrationForm, UserLoginForm, LocationForm, RouteForm, UserEditForm, AdminUserCreationForm

User = get_user_model()

# --- NEW FUNCTION: TOGGLE DRIVER STATUS ---
@login_required
def toggle_driver_status(request):
    if request.user.role == 'DRIVER':
        # Flip the status (True becomes False, False becomes True)
        request.user.is_driver_online = not request.user.is_driver_online
        request.user.save()
        
        status_msg = "Online" if request.user.is_driver_online else "Offline"
        messages.success(request, f"You are now {status_msg}")
        
    return redirect('driver_dashboard')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'DRIVER':
            return redirect('driver_dashboard')
        else:
            return redirect('passenger_dashboard')
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'DRIVER':
                return redirect('driver_dashboard')
            else:
                return redirect('passenger_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'ADMIN' or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'DRIVER':
                return redirect('driver_dashboard')
            else:
                return redirect('passenger_dashboard')
        else:
            messages.error(request, 'Invalid input, please sign in again.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')

# --- DASHBOARD VIEWS ---

# UPDATED: Now sends 'current_ride' to show the Live Status Card
@login_required
def passenger_dashboard(request):
    # Get the current active ride (Pending or Accepted)
    current_ride = Booking.objects.filter(
        passenger=request.user, 
        status__in=['PENDING', 'ACCEPTED']
    ).first()
    
    history = Booking.objects.filter(passenger=request.user, status='COMPLETED').order_by('-created_at')
    
    return render(request, 'passenger/dashboard.html', {'history': history, 'current_ride': current_ride})

@login_required
def driver_dashboard(request):
    # If driver is OFFLINE, they see NO pending bookings
    if request.user.is_driver_online:
        pending_bookings = Booking.objects.filter(status='PENDING')
    else:
        pending_bookings = [] # Empty list because they are offline

    active_ride = Booking.objects.filter(driver=request.user, status='ACCEPTED').first()
    history = Booking.objects.filter(driver=request.user, status='COMPLETED').order_by('-created_at')
    
    context = {
        'pending_bookings': pending_bookings,
        'active_ride': active_ride,
        'history': history
    }
    return render(request, 'driver/dashboard.html', context)

@login_required
def accept_ride(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.status != 'PENDING':
        messages.error(request, "Too late! Another driver has already accepted this ride.")
        return redirect('driver_dashboard')
    
    booking.driver = request.user
    booking.status = 'ACCEPTED'
    booking.save()
    
    # Mark driver as busy
    request.user.is_available = False
    request.user.save()
    
    messages.success(request, "Ride Accepted! Please pick up the passenger.")
    return redirect('driver_dashboard')

# --- NEW FUNCTION: CANCEL RIDE ---
@login_required
def cancel_ride(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    # Only allow cancel if it's the passenger and status is Pending or Accepted
    if request.user == booking.passenger and booking.status in ['PENDING', 'ACCEPTED']:
        booking.status = 'CANCELLED'
        booking.save()
        
        # If a driver was assigned, free them up!
        if booking.driver:
            booking.driver.is_available = True
            booking.driver.save()
            
        messages.success(request, "Ride cancelled successfully.")
    else:
        messages.error(request, "Cannot cancel this ride.")
        
    return redirect('passenger_dashboard')

# --- BOOKING LOGIC ---

@login_required
def book_ride(request):
    if request.method == 'POST':
        source_id = request.POST.get('source')
        dest_id = request.POST.get('destination')
        
        # 1. CHECK AVAILABILITY: Find drivers who are ONLINE and FREE
        online_drivers = User.objects.filter(role='DRIVER', is_driver_online=True)
        available_driver_found = False
        
        for driver in online_drivers:
            # Check if this driver is busy with another ride
            is_busy = Booking.objects.filter(driver=driver, status='ACCEPTED').exists()
            if not is_busy:
                available_driver_found = True
                break

        if not available_driver_found:
            messages.error(request, "⚠️ All drivers are currently busy or offline. Please try again later.")
            return redirect('passenger_dashboard')
        
        # 2. PROCEED IF DRIVER FOUND
        try:
            route = Route.objects.get(source_id=source_id, destination_id=dest_id)
            estimated_price = route.distance_km * 30
            
            Booking.objects.create(
                passenger=request.user,
                source=route.source,
                destination=route.destination,
                estimated_fare=estimated_price,
                status='PENDING'
            )
            messages.success(request, f"Ride Booked! Est. Fare: Rs. {estimated_price}")
            return redirect('passenger_dashboard')
            
        except Route.DoesNotExist:
            messages.error(request, "Sorry, no auto is available for this specific route yet.")
            
    locations = Location.objects.all()
    return render(request, 'passenger/book_ride.html', {'locations': locations})

@login_required
def complete_ride(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    if request.method == 'POST':
        actual_distance = float(request.POST.get('actual_distance'))
        final_fare = actual_distance * 30
        
        booking.actual_distance = actual_distance
        booking.final_fare = final_fare
        booking.status = 'COMPLETED'
        booking.save()
        
        # Mark driver as free again
        request.user.is_available = True
        request.user.save()
        
        messages.success(request, f"Ride Completed! Total Fare: Rs. {final_fare}")
        return redirect('driver_dashboard')
        
    return render(request, 'driver/complete_ride.html', {'booking': booking})

@login_required
def ride_history(request):
    if request.user.role == 'DRIVER':
        rides = Booking.objects.filter(driver=request.user, status='COMPLETED').order_by('-created_at')
    else:
        rides = Booking.objects.filter(passenger=request.user, status='COMPLETED').order_by('-created_at')
    return render(request, 'history.html', {'rides': rides})

@login_required
def view_bill(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    # Allow Admin (superuser) to view bills too!
    if request.user != booking.passenger and request.user != booking.driver and not request.user.is_superuser:
        messages.error(request, "You are not authorized to view this bill.")
        return redirect('home')
    return render(request, 'bill.html', {'booking': booking})

# --- ADMIN CUSTOM VIEWS ---

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_custom/dashboard.html')

@user_passes_test(is_admin)
def admin_add_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "New User Created Successfully!")
            return redirect('admin_dashboard')
    else:
        form = AdminUserCreationForm() 
    return render(request, 'admin_custom/add_user.html', {'form': form})

@user_passes_test(is_admin)
def admin_routes(request):
    routes = Route.objects.all()
    return render(request, 'admin_custom/routes.html', {'routes': routes})

@user_passes_test(is_admin)
def admin_add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route Added Successfully!")
            return redirect('admin_routes')
    else:
        form = RouteForm()
    return render(request, 'admin_custom/add_route.html', {'form': form})

@user_passes_test(is_admin)
def admin_add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Location Added Successfully!")
            return redirect('admin_dashboard')
    else:
        form = LocationForm()
    return render(request, 'admin_custom/add_location.html', {'form': form})

@user_passes_test(is_admin)
def admin_delete_route(request, route_id):
    route = Route.objects.get(id=route_id)
    route.delete()
    messages.success(request, "Route deleted successfully.")
    return redirect('admin_routes')

@user_passes_test(is_admin)
def admin_manage_users(request):
    users = User.objects.filter(is_superuser=False) 
    return render(request, 'admin_custom/manage_users.html', {'users': users})

# --- NEW FUNCTION: ADMIN VIEW USER HISTORY ---
@user_passes_test(is_admin)
def admin_user_history(request, user_id):
    user_obj = User.objects.get(id=user_id)
    
    # Check if they are a Driver or Passenger to get correct history
    if user_obj.role == 'DRIVER':
        rides = Booking.objects.filter(driver=user_obj).order_by('-created_at')
        total_earned = sum(r.final_fare for r in rides if r.final_fare)
        context = {'target_user': user_obj, 'rides': rides, 'total': total_earned, 'type': 'Earned'}
    else:
        # Default to Passenger logic
        rides = Booking.objects.filter(passenger=user_obj).order_by('-created_at')
        total_spent = sum(r.final_fare for r in rides if r.final_fare)
        context = {'target_user': user_obj, 'rides': rides, 'total': total_spent, 'type': 'Spent'}
        
    return render(request, 'admin_custom/user_history.html', context)

@user_passes_test(is_admin)
def admin_edit_user(request, user_id):
    user_obj = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user_obj.username} updated successfully!")
            return redirect('admin_manage_users')
    else:
        form = UserEditForm(instance=user_obj)
    return render(request, 'admin_custom/edit_user.html', {'form': form, 'user_obj': user_obj})

@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    user_obj = User.objects.get(id=user_id)
    user_obj.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('admin_manage_users')

@user_passes_test(is_admin)
def admin_edit_route(request, route_id):
    route = Route.objects.get(id=route_id)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, "Route updated successfully!")
            return redirect('admin_routes')
    else:
        form = RouteForm(instance=route)
    return render(request, 'admin_custom/edit_route.html', {'form': form, 'route': route})

def route_list(request):
    all_routes = Route.objects.all().order_by('source__name', 'destination__name')
    context = {'routes': all_routes}
    return render(request, 'admin_custom/routes.html', context)