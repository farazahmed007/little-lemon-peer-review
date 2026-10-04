from datetime import date, time, timedelta
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from .models import Booking, Menu


class MenuModelTest(TestCase):
    def test_menu_string(self):
        item = Menu.objects.create(title='Greek Salad', price='12.50', inventory=10)
        self.assertEqual(str(item), 'Greek Salad')


class BookingModelTest(TransactionTestCase):
    def test_booking_string(self):
        item = Booking.objects.create(
            first_name='Test',
            reservation_date=date.today() + timedelta(days=1),
            reservation_slot=time(19, 0),
        )
        self.assertIn('Test', str(item))

    def test_duplicate_date_and_slot_rejected(self):
        d = date.today() + timedelta(days=1)
        Booking.objects.create(first_name='A', reservation_date=d, reservation_slot=time(19, 0))
        with self.assertRaises(IntegrityError):
            Booking.objects.create(first_name='B', reservation_date=d, reservation_slot=time(19, 0))
