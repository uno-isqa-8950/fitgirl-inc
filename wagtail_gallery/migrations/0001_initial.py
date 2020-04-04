from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category name')),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='wagtail_gallery.Category', verbose_name='Parent category')),
            ],
            options={
                'verbose_name': 'Gallery Category',
                'verbose_name_plural': 'Gallery Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CategoryGalleryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtail_gallery.Category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='GalleryParentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True, help_text='Text to appear on gallery root page', verbose_name='Body')),
            ],
            options={
                'verbose_name': 'Gallery Root Page',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='GalleryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True, help_text='Body of text on page', verbose_name='Body')),
                ('description', models.TextField(blank=True, help_text='Short description of gallery', null=True, verbose_name='Description')),
                ('categories', models.ManyToManyField(blank=True, help_text='Categories relevant to gallery', through='wagtail_gallery.CategoryGalleryPage', to='wagtail_gallery.Category', verbose_name='Categories')),
            ],
            options={
                'verbose_name': 'Gallery',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('gallery', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_image', to='wagtail_gallery.GalleryPage')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Image')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
       
        migrations.AddField(
            model_name='categorygallerypage',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_categories', to='wagtail_gallery.GalleryPage'),
        ),
        
    ]
