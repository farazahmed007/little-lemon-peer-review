from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from restaurant import views

router = DefaultRouter()
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu-page'),
    path('book/', views.booking_page, name='booking'),
    path('reservations/', views.reservations_page, name='reservations'),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # Legacy endpoints used by the original booking frontend.
    path('api/booking/', views.bookings_api, name='booking-api-legacy'),
    path('api/menu-legacy/', views.menu_api, name='menu-api-legacy'),
    path('api/menu-legacy/<int:item_id>/', views.menu_item_api, name='menu-item-api-legacy'),
    path('api/register/', views.register_api, name='register-api'),
    path('api/login/', views.login_api, name='login-api'),
    path('api/logout/', views.logout_api, name='logout-api'),
]
