# Fitness Studio Booking API

A simple API built with **Django REST Framework** for managing fitness classes and bookings in a fictional fitness studio.

---

## Features

-  View all upcoming fitness classes
-  Create new classes
-  Book a slot in a class
-  View bookings by email
-  Timezone-aware class schedules

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite
- Pytz (for timezone support)

---

## Installation & Setup

```bash
git clone https://github.com/vaisagh-mp/fitness_booking.git
cd fitness-booking-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations and create admin user
python manage.py migrate
python manage.py createsuperuser

# Start the server
python manage.py runserver

---

## API Endpoints

GET /classes/?timezone=<Region/City>

Example Request:

- GET /classes/?timezone=Asia/Kolkata

    [
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Amit",
    "date_time": "2025-06-13T04:00:00Z",
    "local_time": "2025-06-13 09:30 IST",
    "available_slots": 20
  }
]


- POST /classes/create/

Request:

{
  "name": "Zumba",
  "date_time": "2025-06-13T09:00:00Z",
  "instructor": "Riya",
  "total_slots": 20
}

Response:

{
  "id": 1,
  "name": "Zumba",
  "date_time": "2025-06-13T09:00:00Z",
  "instructor": "Riya",
  "total_slots": 20,
  "available_slots": 20
}


- POST /book/
Books a client into a class. Decrements available_slots.

Request:
{
  "class_id": 1,
  "client_name": "Raju Lal",
  "client_email": "raju@example.com"
}

Response:

{
  "id": 5,
  "fitness_class": 1,
  "client_name": "Raju Lal",
  "client_email": "raju@example.com",
  "booked_at": "2025-06-11T05:22:30.123Z"
}

Errors:

{
  "error": "No slots available."
}


- GET /bookings/?email=client@example.com
Returns all bookings made by a given email.

Request:
GET /bookings/?email=raju@example.com

Response:
[
  {
    "id": 5,
    "fitness_class": 1,
    "client_name": "John Doe",
    "client_email": "raju@example.com",
    "booked_at": "2025-06-11T05:22:30.123Z"
  }
]
