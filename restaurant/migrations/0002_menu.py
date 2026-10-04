from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("restaurant", "0001_initial")]
    operations = [migrations.CreateModel(name="Menu", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=100)), ("price", models.DecimalField(decimal_places=2, max_digits=6)), ("inventory", models.PositiveIntegerField(default=0))], options={"ordering": ["title"]})]
