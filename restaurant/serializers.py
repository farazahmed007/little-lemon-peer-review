from rest_framework import serializers
from .models import Menu, Booking


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        reservation_date = attrs.get('reservation_date')
        reservation_slot = attrs.get('reservation_slot')
        if reservation_date and reservation_date < __import__('datetime').date.today():
            raise serializers.ValidationError('You cannot book a past date.')
        if reservation_date and reservation_slot and Booking.objects.filter(
            reservation_date=reservation_date, reservation_slot=reservation_slot
        ).exists():
            raise serializers.ValidationError('This reservation slot is already booked for the selected date.')
        return attrs
