# Generated by Django 2.0.8 on 2019-03-20 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_kindnessmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kindnessmessage',
            old_name='created_at',
            new_name='created_date',
        ),
    ]