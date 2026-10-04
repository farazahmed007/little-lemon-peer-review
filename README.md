# Little Lemon Web Application

Django-based Little Lemon restaurant application for peer review.

## Features
- Django serves static HTML templates, CSS and JavaScript.
- MySQL database configuration through `.env`.
- Menu model and Menu API.
- Table booking model and Booking API with date/slot duplicate protection.
- User registration, login and logout APIs using Django authentication.
- Django admin for menu and bookings.
- Unit tests for pages, APIs, bookings and authentication.
- APIs can be tested with Insomnia or any REST client.

## API paths for peer testing
- `GET/POST /api/menu/`
- `GET/DELETE /api/menu/<id>/`
- `GET/POST /api/bookings/`
- `GET/POST /api/booking/` (alias)
- `POST /api/register/`
- `POST /api/login/`
- `GET /api/logout/`

## Setup
1. Create a MySQL database named `littlelemon`.
2. Copy `.env.example` to `.env` and configure MySQL credentials.
3. `pipenv install`
4. `pipenv shell`
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py test`
8. `python manage.py runserver`
