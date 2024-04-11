# -*- coding: utf-8 -*-
# Generated by Django 4.2.6 on 2024-02-24 13:16

import uuid

import django.core.validators
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_id_alter_discount_id_alter_product_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('code', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=8, max_length=8, prefix='', unique=True)),
                ('percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
