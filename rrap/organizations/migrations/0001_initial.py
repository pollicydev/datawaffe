# Generated by Django 3.2.15 on 2022-11-26 09:17

from django.db import migrations, models
import rrap.organizations.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=255, verbose_name='name')),
                ('title', models.CharField(max_length=400, unique=True, verbose_name='title')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('acronym', models.CharField(blank=True, max_length=10, null=True)),
                ('about', models.TextField(blank=True, max_length=400, null=True)),
                ('logo', models.ImageField(blank=True, upload_to=rrap.organizations.models.get_logo_full_path)),
                ('logo_version', models.IntegerField(blank=True, default=0, editable=False)),
                ('website', models.URLField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('org_type', models.CharField(blank=True, choices=[('individual', 'Individual'), ('donor', 'Donor'), ('government', 'Government'), ('int_ngo', 'International NGO'), ('cso', 'Civil Society Organization'), ('private_sector', 'Private sector'), ('religious', 'Religious'), ('other', 'Other')], max_length=20, verbose_name='Type of organization')),
                ('status', models.SmallIntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (0, 'Not verified'), (3, 'Disabled'), (4, 'Suspended')], default=0)),
                ('locations', models.ManyToManyField(related_name='organizations', to='core.Location')),
            ],
            options={
                'verbose_name_plural': 'organizations',
                'ordering': ['name'],
            },
        ),
    ]
