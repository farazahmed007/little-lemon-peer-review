from datetime import date, time, timedelta
import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Booking, Menu

class LittleLemonTests(TestCase):
    def test_home_serves_html(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Lemon')

    def test_menu_api(self):
        Menu.objects.create(title='Greek Salad', price='12.50', inventory=10)
        response = self.client.get(reverse('menu-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['title'], 'Greek Salad')

    def test_booking_api_and_duplicate_protection(self):
        tomorrow = date.today() + timedelta(days=1)
        payload = {'first_name':'Test','reservation_date':tomorrow.isoformat(),'reservation_slot':'19:00','number_of_guests':2,'occasion':'Birthday'}
        first = self.client.post(reverse('bookings-api'), data=json.dumps(payload), content_type='application/json')
        second = self.client.post(reverse('bookings-api'), data=json.dumps(payload), content_type='application/json')
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_registration_and_login(self):
        response = self.client.post(reverse('register-api'), data=json.dumps({'username':'learner','password':'StrongPass123!','email':'learner@example.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('login-api'), data=json.dumps({'username':'learner','password':'StrongPass123!'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['message'].startswith('Login'))

    def test_booking_filter_by_date(self):
        tomorrow = date.today() + timedelta(days=1)
        Booking.objects.create(first_name='A', reservation_date=tomorrow, reservation_slot=time(18, 0))
        Booking.objects.create(first_name='B', reservation_date=tomorrow + timedelta(days=1), reservation_slot=time(18, 0))
        response = self.client.get(reverse('bookings-api'), {'date': tomorrow.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
