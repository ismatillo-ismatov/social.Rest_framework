# Generated by Django 3.2.9 on 2021-12-01 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=1200),
        ),
    ]