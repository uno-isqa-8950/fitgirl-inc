# Generated by Django 2.2.4 on 2020-05-03 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloneprograminfo',
            name='KCardTemplate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.KindnessCardTemplate'),
        ),
    ]
