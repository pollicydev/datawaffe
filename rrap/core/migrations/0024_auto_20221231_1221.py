# Generated by Django 3.2.15 on 2022-12-31 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20221230_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationpage',
            name='has_microdata',
            field=models.BooleanField(default=False, verbose_name='Contains microdata e.g household survey results, disaggregated needs assessment data, etc'),
        ),
        migrations.AddField(
            model_name='publicationpage',
            name='has_pii',
            field=models.BooleanField(default=False, verbose_name='Contains Personally Identifiable Information (PII) e.g names, phone numbers, Identification number, etc'),
        ),
        migrations.AddField(
            model_name='publicationpage',
            name='privacy',
            field=models.SmallIntegerField(choices=[(0, 'By request (Anyone can search and view the metadata of this dataset. Registered users can submit a request to obtain the data directly from you, by email, file transfer, etc.)'), (1, 'Private (Only you and other members of your organisation can search, view/edit or download this dataset)'), (2, 'Public (Anyone can search, view/edit or download this dataset)')], default=2, verbose_name='Privacy setting'),
        ),
    ]
