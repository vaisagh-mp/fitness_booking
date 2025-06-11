import pytz
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, FitnessClassCreateSerializer
from django.utils.timezone import now

class FitnessClassCreateView(generics.CreateAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassCreateSerializer

class FitnessClassListView(APIView):
    def get(self, request):
        timezone_str = request.GET.get('timezone', 'UTC')
        try:
            user_tz = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            return Response({"error": "Invalid timezone"}, status=400)

        classes = FitnessClass.objects.all()
        data = []
        for cls in classes:
            local_dt = cls.date_time.astimezone(user_tz)
            data.append({
                "id": cls.id,
                "name": cls.name,
                "instructor": cls.instructor,
                "date_time": cls.date_time.isoformat(),
                "local_time": local_dt.strftime("%Y-%m-%d %H:%M %Z"),
                "available_slots": cls.available_slots,
            })
        return Response(data)

class BookingCreateView(APIView):
    def post(self, request):
        class_id = request.data.get("class_id")
        name = request.data.get("client_name")
        email = request.data.get("client_email")

        if not all([class_id, name, email]):
            return Response({"error": "Missing required fields."}, status=400)

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Fitness class not found."}, status=404)

        if fitness_class.available_slots < 1:
            return Response({"error": "No slots available."}, status=400)

        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=name,
            client_email=email
        )

        fitness_class.available_slots -= 1
        fitness_class.save()

        return Response(BookingSerializer(booking).data, status=201)

class BookingListView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        bookings = Booking.objects.filter(client_email=email).order_by('-booked_at')
        return Response(BookingSerializer(bookings, many=True).data)
