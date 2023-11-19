# Generated by Django 4.2.7 on 2023-11-19 18:50

import MaasApp.models.payment
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MaasApp', '0002_location_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('datetime', models.DateTimeField()),
                ('status', django_enumfield.db.fields.EnumField(enum=MaasApp.models.payment.PaymentStatus)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MaasApp.user')),
            ],
        ),
    ]