# Generated by Django 3.2.15 on 2022-12-15 13:22

import django.core.validators
from django.db import migrations, models
import rrap.organizations.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0016_auto_20221215_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityreach',
            name='period',
            field=models.PositiveSmallIntegerField(blank=True, default=2022, help_text='Enter year of record', null=True, validators=[django.core.validators.MinValueValidator(2000), rrap.organizations.models.max_value_current_year]),
        ),
        migrations.AlterField(
            model_name='violenceentry',
            name='period',
            field=models.PositiveSmallIntegerField(blank=True, default=2022, help_text='Enter year of record', null=True, validators=[django.core.validators.MinValueValidator(2000), rrap.organizations.models.max_value_current_year]),
        ),
    ]
