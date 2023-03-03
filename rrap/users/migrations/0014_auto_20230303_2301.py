# Generated by Django 3.2.15 on 2023-03-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_affiliated_ukpc'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_ukpc_affiliate',
            field=models.SmallIntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1, verbose_name='Is the organisation you are affiliated too a member of UKPC?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='affiliated_ukpc',
            field=models.BooleanField(default=True, verbose_name='Is the organisation you are affiliated to a member of UKPC?'),
        ),
    ]
