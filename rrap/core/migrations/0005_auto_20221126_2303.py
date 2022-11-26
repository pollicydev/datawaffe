# Generated by Django 3.2.15 on 2022-11-26 20:03

from django.db import migrations
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_issues_keypopulation_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='keypopulation',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='keypopulation',
            name='color',
            field=wagtail_color_panel.fields.ColorField(default='#000000', max_length=7),
        ),
    ]
