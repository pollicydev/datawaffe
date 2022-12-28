# Generated by Django 3.2.15 on 2022-12-28 10:17

import django.core.validators
from django.db import migrations, models
import modelcluster.fields
import rrap.organizations.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_publicationtype'),
        ('organizations', '0020_alter_organisationpublication_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationpublication',
            name='pub_types',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='core.PublicationType'),
        ),
        migrations.AddField(
            model_name='organisationpublication',
            name='summary',
            field=models.TextField(blank=True, help_text='Summarize publication in one paragraph (max 300 chars)', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='organisationpublication',
            name='title',
            field=models.CharField(blank=True, help_text='Title of publication (max 200 chars)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organisationpublication',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, default=2022, help_text='Year published', null=True, validators=[django.core.validators.MinValueValidator(2000), rrap.organizations.models.max_value_current_year]),
        ),
    ]
