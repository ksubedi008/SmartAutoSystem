Smart Auto System A Modern Auto-Rickshaw Booking Management System**

Smart Auto System is a Django-based web application designed to bridge the gap between auto-rickshaw drivers and passengers. It features a real-time booking flow, automated fare calculation based on distance, and a sleek, modern glass-morphism UI.
Features
Passenger Features
Real-time Booking: Select source and destination from available routes.
Fare Estimation: View estimated costs before booking (calculated at Rs. 30/km).
Live Status: Track if a ride is pending or accepted by a driver.
Trip History: View a modern list of all past trips with digital receipts.
Driver Features
Online/Offline Toggle: Control availability with a single click.
Request Management: View and accept new passenger requests in real-time.
Ride Completion: Enter actual distance traveled to generate final bills.
Earnings History: Access a detailed log of all completed trips and fares.
Admin Features
User Management: Create, edit, and delete drivers or passengers.
Route Control: Manage locations and set distances between routes.
System Oversight: View global trip history and system analytics.
Technical Setup (Windows)
Follow these steps exactly to get the project running on your local machine.

1. Change Directory
Open your Command Prompt (CMD) and navigate to your project folder:

cd path\to\your\SmartAutoSystem

2. Create Virtual Environment
Create an isolated environment to keep the project dependencies organized:
DOS

python -m venv venv

3. Start (Activate) Virtual Environment

Activate the environment so your terminal uses the local Python settings:
DOS

venv\Scripts\activate

(You should see (venv) appear at the beginning of your command prompt line.)
4. Install Dependencies

Install Django and other required libraries:
DOS

pip install django

5. Database Migrations

Set up the database tables:
DOS

python manage.py makemigrations
python manage.py migrate

6. Start the Server

Run the project locally:
DOS

python manage.py runserver

Access the site at: http://127.0.0.1:8000/
 External Testing (ngrok)

To test the system with friends or on mobile devices:

    Ensure the server is running (runserver).

    Open a new CMD window and type:
    DOS

    ngrok http 8000

    Share the https://... link provided by ngrok.

    Note: Ensure your settings.py has ALLOWED_HOSTS = ['*'] or your specific ngrok domain.

 UI/UX Design
    Framework: Bootstrap 5.3
    Theme: Dark Mode / Glass-morphism
    Icons: FontAwesome 6.4
    Fonts: Poppins (Google Fonts)
Developer
    Name: k_subedi08
    Project: BCA 4th Semester Project (2026)
    Contact: +977 9820523224


Project Summary:

The Smart Auto System is a sophisticated web-based management platform developed as a BCA 4th Semester Project. It is designed to modernize and streamline the interaction between auto-rickshaw drivers and passengers through an intuitive, real-time booking environment.

Objective

The primary goal of this project is to eliminate the traditional "wait-and-search" method for auto-rickshaws by providing a digital interface where passengers can find available drivers and drivers can manage their trips efficiently.

Core Functionality
    Real-time Booking Workflow: Passengers can select predefined routes, receive fare estimates, and book rides instantly.
    Driver Availability Management: Drivers have the autonomy to toggle their status between "Online" and "Offline," ensuring they only receive requests when ready.
    Automated Billing: The system calculates fares based on a rate of Rs. 30/km, generating a digital receipt upon trip completion.
    Trip History & Record Keeping: Both drivers and passengers can access a modern history log of all past completed trips, complete with bill viewing options.

 Design & User Experience
The application utilizes a modern glass-morphism UI with a deep purple and blue color palette. Key design features include:
    Symmetrical Pill-Shaped UI: Authentication and navigation buttons are designed as perfectly aligned ovals for a professional aesthetic.
    Responsive Dashboard: Tailored views for Drivers, Passengers, and Admins that adapt to both desktop and mobile screens.
    Fast Notifications: System alerts (success/error messages) are optimized with a 1-second display time and a slide-up animation for a snappy feel.
Technical Stack
    Backend: Python / Django.
    Frontend: HTML5, CSS3 (Custom Styling), and Bootstrap 5.3.
    Database: SQLite (Default Django) for storing user roles, routes, and booking data.
    Security: Role-based access control (RBAC) ensuring that only authorized users can access specific dashboards or view sensitive bills.



Project Conclusion

The Smart Auto System successfully demonstrates the potential of digital transformation in the local transportation sector. By integrating a user-friendly interface with a robust Django backend, the project provides a reliable solution for real-time booking, driver management, and automated fare calculation.

The implementation of a role-based dashboard system ensures that users—whether passengers, drivers, or administrators—interact with a clean and focused environment tailored to their specific needs. The modern design, characterized by its glass-morphism aesthetic and symmetrical UI elements, ensures that the system is not only functional but also visually competitive with contemporary mobile applications. Ultimately, this project serves as a solid foundation for a scalable, real-world ride-hailing platform.
 Future Enhancements

While the current version of the Smart Auto System covers all essential features for a semester project, the following enhancements could be integrated for a production-level release:

    Real-time GPS Tracking: Integration with the Google Maps API or OpenStreetMap to track the live location of autos on the passenger dashboard.

    Integrated Payment Gateway: Incorporation of payment APIs (like Khalti, eSewa, or Stripe) to allow passengers to pay directly through the app instead of just viewing a bill.

    Push Notifications: Implementation of WebSockets or Firebase to send instant notifications to drivers when a new ride is requested, rather than relying on page refreshes.

    Rating & Review System: A feature allowing passengers to rate drivers and leave feedback, which would then be visible in the driver's profile and history.

    Driver Analytics: An advanced dashboard for drivers to view daily, weekly, and monthly earnings charts and trip statistics.

    Mobile App Version: Transitioning the web-based system into a cross-platform mobile application using Flutter or React Native for better accessibility on the go.
