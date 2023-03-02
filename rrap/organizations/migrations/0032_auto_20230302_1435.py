# Generated by Django 3.2.15 on 2023-03-02 11:35

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_swkeypopulation_swservice_swviolation'),
        ('organizations', '0031_auto_20230302_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sexworkorganisation',
            name='gender',
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='locations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.Location', verbose_name='Where do you work? (select all districts that apply)'),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='needs_priorities',
            field=models.TextField(blank=True, help_text='e.g. disability-specific services, mental health support, etc. Write freely. Max 2000 characters', max_length=2000, null=True, verbose_name="What are the organisation's needs and priorities?"),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='support_pwds',
            field=models.BooleanField(blank=True, default=True, help_text='Check the box if Yes', verbose_name='Does the organisation actively support Persons with Disability(PWDs)?'),
        ),
    ]
