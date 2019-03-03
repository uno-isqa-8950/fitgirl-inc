# Generated by Django 2.0.8 on 2019-03-02 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('week', '0010_merge_20190222_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='KindnessCardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('KindnessCard', models.CharField(blank=True, max_length=10000)),
                ('KindnessCard2', models.CharField(blank=True, max_length=10000)),
                ('KindnessCard3', models.CharField(blank=True, max_length=10000)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]