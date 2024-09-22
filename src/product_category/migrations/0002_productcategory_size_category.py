# Generated by Django 5.0.7 on 2024-08-26 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_product_category', '0001_initial'),
        ('src_size_category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='size_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='src_size_category.sizecategory'),
        ),
    ]