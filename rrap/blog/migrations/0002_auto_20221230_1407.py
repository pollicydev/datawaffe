# Generated by Django 3.2.15 on 2022-12-30 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpage',
            options={'ordering': ['date', 'title'], 'verbose_name': 'Blog', 'verbose_name_plural': 'Blogs'},
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author',
        ),
    ]
