# Generated by Django 3.2.15 on 2022-12-29 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('core', '0019_delete_previewabledocument'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MapPage',
        ),
    ]
