# Generated by Django 3.2.9 on 2021-12-01 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(default=None, max_length=1200),
        ),
    ]
