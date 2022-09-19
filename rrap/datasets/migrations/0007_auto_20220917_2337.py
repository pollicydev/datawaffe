# Generated by Django 3.2.15 on 2022-09-17 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0006_auto_20220917_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[(0, 'Draft'), (1, 'Published')], default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='methodology',
            field=models.CharField(choices=[(0, 'Census'), (1, 'Sample survey'), (2, 'Direct observational/Anecdotal data'), (3, 'Registry'), (4, 'Other')], default=1, max_length=20, verbose_name='Data methodology'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='update_frequency',
            field=models.CharField(choices=[(0, 'Every week'), (1, 'Every two weeks'), (2, 'Every month'), (3, 'Every three months'), (4, 'Every six months'), (5, 'Every year'), (6, 'As needed'), (7, 'Never')], default=6, max_length=20, verbose_name='Update frequency'),
        ),
    ]
