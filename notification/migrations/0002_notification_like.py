# Generated by Django 5.1.2 on 2025-06-17 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
        ('votes', '0002_like_delete_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='like',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votes.like'),
        ),
    ]
