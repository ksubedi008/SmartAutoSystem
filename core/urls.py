from django.urls import path
from . import views

urlpatterns = [
    # --- The Original Homepage ---
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard Routes
    path('passenger-dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    
    # --- MAIN FEATURES ---
    path('book-ride/', views.book_ride, name='book_ride'),
    path('accept-ride/<int:booking_id>/', views.accept_ride, name='accept_ride'),
    path('complete-ride/<int:booking_id>/', views.complete_ride, name='complete_ride'),
    path('history/', views.ride_history, name='ride_history'),
    path('bill/<int:booking_id>/', views.view_bill, name='view_bill'),
    
    # NEW: Driver Status Toggle (Online/Offline) -> This was missing!
    path('toggle-status/', views.toggle_driver_status, name='toggle_driver_status'),
    
    # Admin Routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-add-user/', views.admin_add_user, name='admin_add_user'),
    path('admin-routes/', views.admin_routes, name='admin_routes'),
    path('admin-add-route/', views.admin_add_route, name='admin_add_route'),
    path('admin-add-location/', views.admin_add_location, name='admin_add_location'),
    path('admin-delete-route/<int:route_id>/', views.admin_delete_route, name='admin_delete_route'),
    
    # User Management (Fixed Duplicates)
    path('admin-manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin-edit-user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin-delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    
    path('admin-edit-route/<int:route_id>/', views.admin_edit_route, name='admin_edit_route'),
    path('all-routes/', views.route_list, name='all_routes'),
    path('admin-manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin-user-history/<int:user_id>/', views.admin_user_history, name='admin_user_history'),
    path('admin-edit-user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('cancel-ride/<int:booking_id>/', views.cancel_ride, name='cancel_ride'),
    
    # Static Info Pages
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]