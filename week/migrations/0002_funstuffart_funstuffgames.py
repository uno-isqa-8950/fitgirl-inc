# Generated by Django 2.2.10 on 2020-04-27 18:26

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('week', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunStuffGames',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('callout_intro', wagtail.core.fields.RichTextField(blank=True)),
                ('callout_message', wagtail.core.fields.RichTextField(blank=True)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('display_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FunStuffArt',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('callout_intro', wagtail.core.fields.RichTextField(blank=True)),
                ('callout_message', wagtail.core.fields.RichTextField(blank=True)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('display_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
