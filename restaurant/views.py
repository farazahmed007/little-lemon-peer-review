import json
from datetime import date, datetime, time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer

AVAILABLE_SLOTS = [time(hour=h) for h in range(17, 23)]


def home(request):
    return render(request, 'restaurant/home.html')


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'restaurant/about.html')


def menu(request):
    return render(request, 'restaurant/menu.html', {'menu_items': Menu.objects.all()})


def booking_page(request):
    return render(request, 'restaurant/booking.html', {'today': date.today().isoformat()})


def reservations_page(request):
    return render(request, 'restaurant/reservations.html', {'today': date.today().isoformat()})


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        requested_date = self.request.query_params.get('date')
        if requested_date:
            try:
                parsed = datetime.strptime(requested_date, '%Y-%m-%d').date()
            except ValueError:
                return Booking.objects.none()
            return queryset.filter(reservation_date=parsed)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {'detail': 'This reservation slot is already booked for the selected date.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


# Legacy JSON endpoints retained for the booking frontend and peer testing.
def _serialize_booking(b):
    return {
        'id': b.id,
        'first_name': b.first_name,
        'reservation_date': b.reservation_date.isoformat(),
        'reservation_slot': b.reservation_slot.strftime('%H:%M'),
        'number_of_guests': b.number_of_guests,
        'occasion': b.occasion,
    }


def _parse_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return None


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def bookings_api(request):
    if request.method == 'GET':
        requested_date = request.GET.get('date')
        if requested_date:
            parsed = _parse_date(requested_date)
            if parsed is None:
                return JsonResponse({'error': 'Invalid date. Use YYYY-MM-DD.'}, status=400)
            bookings = Booking.objects.filter(reservation_date=parsed)
        else:
            bookings = Booking.objects.all()
        return JsonResponse([_serialize_booking(b) for b in bookings], safe=False)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    first_name = str(payload.get('first_name', '')).strip()
    reservation_date = _parse_date(payload.get('reservation_date'))
    slot_raw = str(payload.get('reservation_slot', '')).strip()
    occasion = str(payload.get('occasion', 'Birthday')).strip()
    try:
        guests = int(payload.get('number_of_guests', 1))
    except (TypeError, ValueError):
        guests = 0
    if not first_name:
        return JsonResponse({'error': 'First name is required.'}, status=400)
    if reservation_date is None:
        return JsonResponse({'error': 'A valid reservation date is required.'}, status=400)
    if reservation_date < date.today():
        return JsonResponse({'error': 'You cannot book a past date.'}, status=400)
    try:
        slot = datetime.strptime(slot_raw, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Invalid reservation slot.'}, status=400)
    if slot not in AVAILABLE_SLOTS:
        return JsonResponse({'error': 'Please choose a valid reservation slot.'}, status=400)
    if guests < 1 or guests > 10:
        return JsonResponse({'error': 'Number of guests must be between 1 and 10.'}, status=400)
    if occasion not in dict(Booking.OCCASIONS):
        return JsonResponse({'error': 'Invalid occasion.'}, status=400)
    try:
        booking = Booking.objects.create(
            first_name=first_name,
            reservation_date=reservation_date,
            reservation_slot=slot,
            number_of_guests=guests,
            occasion=occasion,
        )
    except IntegrityError:
        return JsonResponse({'error': 'This reservation slot is already booked for the selected date.'}, status=409)
    return JsonResponse(_serialize_booking(booking), status=201)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def menu_api(request):
    if request.method == 'GET':
        return JsonResponse(
            [{'id': m.id, 'title': m.title, 'price': str(m.price), 'inventory': m.inventory} for m in Menu.objects.all()],
            safe=False,
        )
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    title = str(payload.get('title', '')).strip()
    try:
        price = float(payload.get('price', 0))
        inventory = int(payload.get('inventory', 0))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid price or inventory.'}, status=400)
    if not title or price < 0 or inventory < 0:
        return JsonResponse({'error': 'Title, price and inventory must be valid.'}, status=400)
    item = Menu.objects.create(title=title, price=price, inventory=inventory)
    return JsonResponse({'id': item.id, 'title': item.title, 'price': str(item.price), 'inventory': item.inventory}, status=201)


def menu_item_api(request, item_id):
    try:
        item = Menu.objects.get(pk=item_id)
    except Menu.DoesNotExist:
        return JsonResponse({'error': 'Menu item not found.'}, status=404)
    if request.method == 'GET':
        return JsonResponse({'id': item.id, 'title': item.title, 'price': str(item.price), 'inventory': item.inventory})
    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'message': 'Menu item deleted.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
@require_http_methods(['POST'])
def register_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', ''))
    email = str(data.get('email', '')).strip()
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists.'}, status=409)
    user = User.objects.create_user(username=username, password=password, email=email)
    return JsonResponse({'message': 'Registration successful.', 'username': user.username}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def login_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    user = authenticate(request, username=data.get('username', ''), password=data.get('password', ''))
    if user is None:
        return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    login(request, user)
    return JsonResponse({'message': 'Login successful.', 'username': user.username})


def logout_api(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully.'})
