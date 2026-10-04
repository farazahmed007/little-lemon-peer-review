from django.contrib import admin
from .models import Booking, Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'inventory')
    search_fields = ('title',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'reservation_date', 'reservation_slot', 'number_of_guests', 'occasion')
    list_filter = ('reservation_date', 'occasion')
