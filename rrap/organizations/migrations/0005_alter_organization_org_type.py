# Generated by Django 3.2.15 on 2022-09-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20220916_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.CharField(blank=True, choices=[('academic', 'Academic/Research'), ('donor', 'Donor'), ('government', 'Government'), ('int_ngo', 'International NGO'), ('int_org', 'International organization'), ('national_org', 'National organization'), ('private_sector', 'Private sector'), ('religious', 'Religious'), ('other', 'Other')], max_length=20, verbose_name='Type of organization'),
        ),
    ]