from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Booking(models.Model):
    OCCASIONS = [
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ('Engagement', 'Engagement'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]
    first_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_slot = models.TimeField()
    number_of_guests = models.PositiveIntegerField(default=1)
    occasion = models.CharField(max_length=20, choices=OCCASIONS, default='Birthday')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reservation_date', 'reservation_slot']
        constraints = [models.UniqueConstraint(fields=['reservation_date', 'reservation_slot'], name='unique_booking_date_slot')]

    def __str__(self):
        return f'{self.first_name} - {self.reservation_date} {self.reservation_slot}'
