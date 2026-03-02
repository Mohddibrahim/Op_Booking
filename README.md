A full-featured Doctor Appointment Booking System built using Django.
This project allows users to register, book appointments, manage doctors, handle payments, and administer the system efficiently.
Features
*User Side

User Registration & Login

Profile Management

Book Appointments

View Appointment History

Online Payment Support

*Doctor Management

Add / Edit / Delete Doctors

Assign Specializations

Manage Doctor Availability

* Appointment System

Book Appointment

Cancel Appointment

Track Status

* Payment Module

Secure Payment Handling

Track Payment Status

* Admin Panel

Manage Users

Manage Doctors

Manage Appointments

Monitor Payments

* Tech Stack

Backend: Django

Frontend: HTML, CSS, Bootstrap

Database: SQLite (Default)

Authentication: Django Built-in Auth System

Project Structure
Booking/
│
├── accounts/         # User authentication
├── doctors/          # Doctor management
├── appointments/     # Appointment booking
├── facilities/       # Facility management
├── payment/          # Payment handling
├── templates/        # HTML Templates
├── static/           # CSS, JS
├── media/            # Uploaded files
├── db.sqlite3
└── manage.py
 Installation Guide
1. Clone Repository
git clone https://github.com/your-username/booking-system.git
cd booking-system
2.Create Virtual Environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install Requirements
pip install -r requirements.txt

If not available:
pip install django
4. Apply Migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser
python manage.py createsuperuser
6. Run Server
python manage.py runserver

Open in browser:

http://127.0.0.1:8000/

Admin Panel:

http://127.0.0.1:8000/admin/
