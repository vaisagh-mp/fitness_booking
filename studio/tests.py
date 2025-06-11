from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .models import FitnessClass, Booking

class FitnessBookingAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.fitness_class = FitnessClass.objects.create(
            name="Zumba",
            instructor="Riya",
            date_time=make_aware(datetime.now() + timedelta(days=1)),
            total_slots=10,
            available_slots=10
        )

    def test_create_fitness_class(self):
        response = self.client.post('/classes/create/', {
            "name": "Yoga",
            "instructor": "Amit",
            "date_time": (datetime.now() + timedelta(days=2)).isoformat(),
            "total_slots": 5
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Yoga")
        self.assertEqual(response.data['available_slots'], 5)

    def test_list_classes_with_timezone(self):
        response = self.client.get('/classes/?timezone=Asia/Kolkata')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("local_time", response.data[0])

    def test_list_classes_invalid_timezone(self):
        response = self.client.get('/classes/?timezone=Invalid/Zone')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid timezone")

    def test_successful_booking(self):
        response = self.client.post('/book/', {
            "class_id": self.fitness_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["client_name"], "John Doe")

        # Refresh class and check if slots reduced
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 9)

    def test_booking_without_required_fields(self):
        response = self.client.post('/book/', {
            "class_id": self.fitness_class.id,
            "client_name": "John Doe"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overbooking(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        response = self.client.post('/book/', {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No slots available.")

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Ravi",
            client_email="ravi@example.com"
        )

        response = self.client.get('/bookings/?email=ravi@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_name'], "Ravi")

    def test_get_bookings_missing_email(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email is required")
