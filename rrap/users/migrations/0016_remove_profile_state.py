# Generated by Django 3.2.15 on 2023-03-05 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_profile_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
    ]
