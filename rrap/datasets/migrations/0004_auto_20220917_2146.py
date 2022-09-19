# Generated by Django 3.2.15 on 2022-09-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20220917_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasetversion',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='datasetversion',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='dataset',
            name='file',
            field=models.FileField(max_length=255, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='dataset',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='url',
            field=models.URLField(default='www.google.com', max_length=3000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DatasetPermission',
        ),
        migrations.DeleteModel(
            name='DatasetVersion',
        ),
    ]
