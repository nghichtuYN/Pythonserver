# Generated by Django 5.0.7 on 2024-08-26 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_size_category', '0002_sizecategory_edited'),
        ('src_size_option', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sizeoption',
            name='size_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='src_size_category.sizecategory'),
        ),
    ]
