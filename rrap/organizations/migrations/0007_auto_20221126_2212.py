# Generated by Django 3.2.15 on 2022-11-26 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20221126_2208'),
        ('organizations', '0006_auto_20221126_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisationpage',
            name='locations',
        ),
        migrations.AddField(
            model_name='organisationpage',
            name='locations',
            field=models.ManyToManyField(related_name='organisations', to='core.Location'),
        ),
    ]
