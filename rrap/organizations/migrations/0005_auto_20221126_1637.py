# Generated by Django 3.2.15 on 2022-11-26 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('organizations', '0004_auto_20221126_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisationpage',
            name='logo_version',
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
