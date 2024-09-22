# Generated by Django 5.0.7 on 2024-08-23 18:17

import django.db.models.deletion
import django.db.models.manager
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('src_brand', '0001_initial'),
        ('src_product_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_name', models.TextField(max_length=255)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('edited', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='src_brand.brand')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src_product_category.productcategory')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
