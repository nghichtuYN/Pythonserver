# Generated by Django 5.0.7 on 2024-08-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_size_category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sizecategory',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
