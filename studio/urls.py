from django.urls import path
from .views import FitnessClassListView, BookingCreateView, BookingListView, FitnessClassCreateView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='classes'),
    path('classes/create/', FitnessClassCreateView.as_view(), name='class-create'),
    path('book/', BookingCreateView.as_view(), name='book'),
    path('bookings/', BookingListView.as_view(), name='bookings'),
]
