# Generated by Django 3.2.15 on 2023-03-04 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20230304_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='affiliated_ukpc',
        ),
    ]
