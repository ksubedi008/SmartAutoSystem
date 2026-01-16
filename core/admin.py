from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Location, Route, Booking

# Custom User Admin to show 'role' column
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'phone_number', 'is_available', 'vehicle_number')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Location)
admin.site.register(Route)
admin.site.register(Booking)