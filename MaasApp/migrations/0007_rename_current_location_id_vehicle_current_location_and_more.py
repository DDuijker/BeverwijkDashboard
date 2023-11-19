# Generated by Django 4.2.7 on 2023-11-19 20:00

import MaasApp.models.payment
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MaasApp', '0006_remove_user_is_dev_remove_user_joined_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='current_location_id',
            new_name='current_location',
        ),
        migrations.AddField(
            model_name='booking',
            name='dropoff_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dropoff_bookings', to='MaasApp.location'),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='MaasApp.payment'),
        ),
        migrations.AddField(
            model_name='booking',
            name='pickup_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pickup_bookings', to='MaasApp.location'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=django_enumfield.db.fields.EnumField(default=0, enum=MaasApp.models.payment.PaymentMethod),
        ),
    ]
