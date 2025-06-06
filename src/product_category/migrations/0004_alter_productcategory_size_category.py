# Generated by Django 5.0.7 on 2024-09-22 01:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_product_category', '0003_productcategory_category_image'),
        ('src_size_category', '0002_sizecategory_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='size_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='src_size_category.sizecategory'),
        ),
    ]
