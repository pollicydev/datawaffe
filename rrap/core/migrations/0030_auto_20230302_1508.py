# Generated by Django 3.2.15 on 2023-03-02 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_delete_issue'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keypopulation',
            options={'verbose_name': 'LGBTQ Key Population', 'verbose_name_plural': 'LGBTQ Key Populations'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'LGBTQ Service', 'verbose_name_plural': 'LGBTQ Services'},
        ),
        migrations.AlterModelOptions(
            name='violation',
            options={'verbose_name': 'LGBTQ Violation', 'verbose_name_plural': 'LGBTQ Violations'},
        ),
    ]
