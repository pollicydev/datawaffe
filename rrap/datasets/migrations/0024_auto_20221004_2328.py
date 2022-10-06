# Generated by Django 3.2.15 on 2022-10-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0023_alter_dataset_doc_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start date'),
        ),
    ]
