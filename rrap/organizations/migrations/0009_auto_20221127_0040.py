# Generated by Django 3.2.15 on 2022-11-26 21:40

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_issues_issue'),
        ('organizations', '0008_auto_20221126_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationpage',
            name='communities',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.KeyPopulation'),
        ),
        migrations.AddField(
            model_name='organisationpage',
            name='issues',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.Issue'),
        ),
        migrations.AddField(
            model_name='organisationpage',
            name='services',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.Service'),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='locations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.Location'),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='topics',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='organisations', to='core.Topic'),
        ),
    ]