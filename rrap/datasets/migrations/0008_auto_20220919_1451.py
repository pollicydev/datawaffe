# Generated by Django 3.2.15 on 2022-09-19 11:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_auto_20220917_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='file',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='mime',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='size',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='url',
        ),
        migrations.CreateModel(
            name='DatasetFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, null=True, upload_to='datasets/')),
                ('url', models.URLField(max_length=3000)),
                ('size', models.IntegerField(default=0)),
                ('mime', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('last_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='last updated')),
                ('note', models.TextField(null=True)),
                ('name', models.CharField(max_length=255)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='datasets.dataset')),
            ],
            options={
                'ordering': ['name', 'created'],
                'get_latest_by': 'created',
            },
        ),
    ]
