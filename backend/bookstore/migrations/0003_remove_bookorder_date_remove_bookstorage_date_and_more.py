# Generated by Django 5.0.3 on 2024-03-19 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_rename_created_account_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookorder',
            name='Date',
        ),
        migrations.RemoveField(
            model_name='bookstorage',
            name='Date',
        ),
        migrations.AddField(
            model_name='consumer',
            name='Debt',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
