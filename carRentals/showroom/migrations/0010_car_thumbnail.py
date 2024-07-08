# Generated by Django 5.0.6 on 2024-07-08 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0009_carimage_alter_reservation_car_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thumbnail_for', to='showroom.carimage'),
        ),
    ]