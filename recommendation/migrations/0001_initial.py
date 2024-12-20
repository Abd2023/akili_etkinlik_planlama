# Generated by Django 5.0.6 on 2024-11-11 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='event_management.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventConflict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conflict_reason', models.CharField(max_length=255)),
                ('conflicting_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflicting_with', to='event_management.event')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflicts', to='event_management.event')),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_interests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
