Little Lemon Web Application

Django restaurant application for peer review.

Main peer-review API endpoints:
GET/POST /api/menu/
GET/PUT/PATCH/DELETE /api/menu/<id>/
GET/POST /api/bookings/
GET/PUT/PATCH/DELETE /api/bookings/<id>/
POST /api-token-auth/
/auth/users/
/auth/token/login/
/auth/token/logout/

Legacy frontend endpoints:
/api/booking/
/api/register/
/api/login/
/api/logout/

The project uses Django REST Framework, Djoser, MySQL, Django templates, and unit tests.

Setup:
1. Create a MySQL database named littlelemon.
2. Copy .env.example to .env and set MySQL credentials.
3. pipenv install
4. pipenv shell
5. python manage.py migrate
6. python manage.py test
7. python manage.py runserver

The browsable Django REST Framework API is available from the /api/ endpoints when the server is running.
