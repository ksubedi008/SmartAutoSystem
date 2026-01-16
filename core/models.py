from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. CUSTOM USER MODEL (Handles Roles & Availability)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PASSENGER', 'Passenger'),
        ('DRIVER', 'Driver'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PASSENGER')
    phone_number = models.CharField(max_length=15, blank=True)
    
    # --- DRIVER SPECIFIC FIELDS ---
    
    # 1. Master Switch: Is the driver currently working? (Clocked In/Out)
    is_driver_online = models.BooleanField(default=False) 
    
    # 2. Availability: Are they free right now? (True = Free, False = Driving someone)
    is_available = models.BooleanField(default=True) 
    
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# 2. LOCATION & ROUTE (For Fare Estimation)
class Location(models.Model):
    name = models.CharField(max_length=100) # e.g., "Dhulabari", "Kakarvitta"

    def __str__(self):
        return self.name

class Route(models.Model):
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='source_routes')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dest_routes')
    distance_km = models.FloatField() # e.g., 5.5
    
    class Meta:
        unique_together = ('source', 'destination') # Prevent duplicate routes

    def __str__(self):
        return f"{self.source} to {self.destination} ({self.distance_km}km)"

# 3. BOOKING SYSTEM
class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_bookings')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_trips')
    
    source = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='pickup_bookings')
    destination = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='drop_bookings')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Financials
    estimated_fare = models.FloatField(default=0.0)
    actual_distance = models.FloatField(null=True, blank=True) # Driver enters this
    final_fare = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ride #{self.id} - {self.status}"