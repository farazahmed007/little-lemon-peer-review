from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('reservation_date', models.DateField()),
                ('reservation_slot', models.TimeField()),
                ('number_of_guests', models.PositiveIntegerField(default=1)),
                ('occasion', models.CharField(choices=[('Birthday', 'Birthday'), ('Anniversary', 'Anniversary'), ('Engagement', 'Engagement'), ('Business', 'Business'), ('Other', 'Other')], default='Birthday', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['reservation_date', 'reservation_slot'],
                'constraints': [
                    models.UniqueConstraint(fields=('reservation_date', 'reservation_slot'), name='unique_booking_date_slot'),
                ],
            },
        ),
    ]
