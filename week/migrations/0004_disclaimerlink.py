# Generated by Django 2.0.8 on 2019-02-09 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('week', '0003_disclaimerpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disclaimerlink',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('disclaimer', models.CharField(blank=True, max_length=10000)),
                ('disclaimer2', models.CharField(blank=True, max_length=10000)),
                ('disclaimer3', models.CharField(blank=True, max_length=10000)),
                ('disclaimer4', models.CharField(blank=True, max_length=10000)),
                ('disclaimer5', models.CharField(blank=True, max_length=10000)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
