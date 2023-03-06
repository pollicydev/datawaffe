# Generated by Django 3.2.15 on 2023-03-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230301_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='other_pronouns',
            field=models.CharField(blank=True, help_text='Please specify your pronouns if missing', max_length=255, null=True, verbose_name='Other pronouns'),
        ),
    ]