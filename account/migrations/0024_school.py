# Generated by Django 2.1.7 on 2019-04-06 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_auto_20190406_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_id', models.AutoField(primary_key=True, serialize=False)),
                ('school_name', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
    ]
