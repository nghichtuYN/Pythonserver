# Generated by Django 5.0.7 on 2024-09-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_orders', '0005_remove_orders_status_orders_ispaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
