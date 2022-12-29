# Generated by Django 3.2.15 on 2022-12-29 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.contrib.taggit
import modelcluster.fields
import rrap.blog.models
import wagtail.contrib.routable_page.models
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailcore', '0066_collection_management_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0024_organisationpublication_thumbnail'),
        ('core', '0020_delete_mappage'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('introduction', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='This date may be displayed on the blog post. It is not used to schedule posts to go live at a later date.', verbose_name='Post date')),
                ('author', models.ForeignKey(blank=True, limit_choices_to=rrap.blog.models.limit_author_choices, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_pages', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_plural', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Blog Page Type',
                'verbose_name_plural': 'Blog Page Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.blogpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_blogpagetag_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogpage',
            name='blog_page_type',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogPageType'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='organisations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='organizations.OrganisationPage'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='topics',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='core.Topic'),
        ),
    ]
