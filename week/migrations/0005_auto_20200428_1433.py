# Generated by Django 2.2.10 on 2020-04-28 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week', '0004_auto_20200428_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensitive',
            name='age_group_content',
            field=models.IntegerField(blank=True, default=0, verbose_name='Enter the age group to show the content to: 1 for 6 or younger; 2  for ages 7-10; 3 for ages 11-13; 4 for ages 14-16; 5 for 17+'),
        ),
    ]
