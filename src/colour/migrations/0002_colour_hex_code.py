# Generated by Django 5.0.7 on 2024-09-15 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_colour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='colour',
            name='hex_code',
            field=models.CharField(blank=True, default=None, max_length=7, null=True),
        ),
    ]
