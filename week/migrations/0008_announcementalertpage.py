# Generated by Django 2.1.7 on 2019-04-04 15:10

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('week', '0007_auto_20190330_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementAlertPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('announcements', wagtail.core.fields.RichTextField(blank=True)),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='End Date')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
