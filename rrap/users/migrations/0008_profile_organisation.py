# Generated by Django 3.2.15 on 2023-03-03 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0034_pwuidscommunityreach'),
        ('users', '0007_alter_profile_organisations'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organisationpage', verbose_name='organisation'),
        ),
    ]
