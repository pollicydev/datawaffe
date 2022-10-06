# Generated by Django 3.2.15 on 2022-10-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0021_dataset_file_mime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='file',
        ),
        migrations.AddField(
            model_name='dataset',
            name='doc_type',
            field=models.SmallIntegerField(choices=[(0, 'Report'), (1, 'Toolkit'), (2, 'Article'), (3, 'Laws'), (4, 'Speech'), (5, 'Video'), (6, 'Audio'), (7, 'Book'), (8, 'Magazine'), (9, 'Artwork'), (10, 'Manua/Guide/Framework')], default=0, verbose_name='Data methodology'),
        ),
    ]
