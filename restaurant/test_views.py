import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from .models import Booking, Menu


class ViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Lemon')

    def test_menu_endpoint(self):
        Menu.objects.create(title='Bruschetta', price='8.50', inventory=5)
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['title'], 'Bruschetta')

    def test_booking_endpoint_and_filter(self):
        d = date.today() + timedelta(days=1)
        payload = {'first_name': 'Test', 'reservation_date': d.isoformat(), 'reservation_slot': '19:00', 'number_of_guests': 2, 'occasion': 'Birthday'}
        response = self.client.post('/api/bookings/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        filtered = self.client.get('/api/bookings/', {'date': d.isoformat()})
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(len(filtered.json()), 1)
