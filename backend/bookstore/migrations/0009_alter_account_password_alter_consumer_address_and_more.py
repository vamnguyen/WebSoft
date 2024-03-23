# Generated by Django 5.0.3 on 2024-03-22 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_alter_account_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='Password',
            field=models.TextField(max_length=12, validators=[django.core.validators.RegexValidator('^(?=.*[A-Za-z])(?=.*\\d)(?=.*[!@#$%^&*()\\-_=+{};:,<.>]).*$'), django.core.validators.MinLengthValidator(6)]),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='Address',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='Name',
            field=models.TextField(max_length=255),
        ),
    ]