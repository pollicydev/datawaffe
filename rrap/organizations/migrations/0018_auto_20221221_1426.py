# Generated by Django 3.2.15 on 2022-12-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0017_auto_20221215_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityreach',
            name='reach',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='How many people in this community did you reach?', null=True),
        ),
        migrations.AlterField(
            model_name='violenceentry',
            name='occurences',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='How many violations of this nature did you deal with?', null=True),
        ),
    ]
