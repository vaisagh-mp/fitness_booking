from django.contrib import admin
from .models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instructor', 'date_time', 'total_slots', 'available_slots')
    list_filter = ('instructor', 'date_time')
    search_fields = ('name', 'instructor')
    ordering = ('date_time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'fitness_class', 'client_name', 'client_email', 'booked_at')
    list_filter = ('fitness_class', 'booked_at')
    search_fields = ('client_name', 'client_email')
    ordering = ('-booked_at',)
