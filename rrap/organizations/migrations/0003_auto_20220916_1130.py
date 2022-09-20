# Generated by Django 3.2.15 on 2022-09-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_topic'),
        ('organizations', '0002_auto_20220916_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name_plural': 'organizations'},
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='description',
            new_name='about',
        ),
        migrations.AddField(
            model_name='organization',
            name='locations',
            field=models.ManyToManyField(to='core.Location'),
        ),
        migrations.AddField(
            model_name='organization',
            name='title',
            field=models.CharField(default='title', max_length=400, unique=True, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.SlugField(max_length=255, verbose_name='name'),
        ),
    ]