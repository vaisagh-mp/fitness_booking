from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils.timezone import localtime


class FitnessClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'total_slots', 'available_slots']
        read_only_fields = ['available_slots'] 


class FitnessClassSerializer(serializers.ModelSerializer):
    local_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'date_time', 'local_time', 'available_slots']

    def get_local_time(self, obj):
        request = self.context.get("request")
        tz = request.query_params.get("timezone", "Asia/Kolkata")
        return localtime(obj.date_time).astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booked_at']
