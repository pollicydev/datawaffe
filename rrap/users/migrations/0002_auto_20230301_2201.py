# Generated by Django 3.2.15 on 2023-03-01 19:01

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='other_pronouns',
            field=models.CharField(blank=True, help_text='Please specify', max_length=255, null=True, verbose_name='Other pronouns'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pronouns',
            field=models.SmallIntegerField(choices=[(0, 'Just my name please!'), (1, 'he/him/his'), (2, 'She/her/hers'), (3, 'They/them/theirs'), (4, 'Ze/hir/hirs'), (5, 'Xe/xem/xyr'), (6, 'She/they'), (7, 'he/they'), (8, 'Other')], default=0, verbose_name='What are your pronouns?'),
        ),
    ]