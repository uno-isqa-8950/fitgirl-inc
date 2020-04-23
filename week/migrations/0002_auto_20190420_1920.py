# Generated by Django 2.1.7 on 2019-04-21 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailmenus', '0022_auto_20170913_2125'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('week', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='rewardspostpage',
            name='display_image',
        ),
        migrations.RemoveField(
            model_name='rewardspostpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='servicepostpage',
            name='display_image',
        ),
        migrations.RemoveField(
            model_name='servicepostpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='testpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='BlogPage',
        ),
        migrations.DeleteModel(
            name='RewardsPostPage',
        ),
        migrations.DeleteModel(
            name='ServicePostPage',
        ),
        migrations.DeleteModel(
            name='TestPage',
        ),
    ]
