# Generated by Django 5.0.6 on 2024-11-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0002_event_latitude_event_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(default=0.0),
            preserve_default=False,
        ),
    ]