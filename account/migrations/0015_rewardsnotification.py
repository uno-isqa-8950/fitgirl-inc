# Generated by Django 2.0.8 on 2019-03-08 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_delete_rewardsnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardsNotification',
            fields=[
                ('rewards_notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('Rewards_milestone_1', models.IntegerField(default=25)),
                ('Rewards_milestone_2', models.IntegerField(default=50)),
                ('Rewards_milestone_3', models.IntegerField(default=75)),
                ('Rewards_milestone_4', models.IntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
    ]