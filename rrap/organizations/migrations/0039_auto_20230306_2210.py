# Generated by Django 3.2.15 on 2023-03-06 19:10

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20230306_1441'),
        ('organizations', '0038_auto_20230306_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lgbtqorganisation',
            name='communities',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='lgbtq_organisations', to='core.LGBTQKeyPopulation', verbose_name='Key Populations Supported'),
        ),
        migrations.AlterField(
            model_name='lgbtqorganisation',
            name='services',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='lgbtq_organisations', to='core.LGBTQService', verbose_name='Services Offered'),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='toll_free',
            field=models.CharField(blank=True, help_text='Toll-free number', max_length=20, null=True, verbose_name='Has toll free'),
        ),
        migrations.AlterField(
            model_name='pwuidsorganisation',
            name='services',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='pwuid_organisations', to='core.PWUIDService', verbose_name='Services Offered'),
        ),
        migrations.AlterField(
            model_name='sexworkorganisation',
            name='communities',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='sw_organisations', to='core.SWKeyPopulation', verbose_name='Key Populations Supported'),
        ),
        migrations.AlterField(
            model_name='sexworkorganisation',
            name='services',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='sw_organisations', to='core.SWService', verbose_name='Services Offered'),
        ),
    ]
