# Generated by Django 5.0.7 on 2024-09-19 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cus_phone',
            field=models.CharField(default=None, max_length=12),
        ),
    ]