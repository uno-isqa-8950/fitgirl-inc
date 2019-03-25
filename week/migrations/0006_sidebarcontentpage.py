# Generated by Django 2.0.8 on 2019-03-24 04:38

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('week', '0005_landingindexpage_additional'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subject_for_announcement1', models.CharField(blank=True, max_length=10000)),
                ('message_announcement1', wagtail.core.fields.RichTextField(blank=True)),
                ('subject_for_announcement2', models.CharField(blank=True, max_length=10000)),
                ('message_announcement2', wagtail.core.fields.RichTextField(blank=True)),
                ('subject_for_announcement3', models.CharField(blank=True, max_length=10000)),
                ('message_announcement3', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]