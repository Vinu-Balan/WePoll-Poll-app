# Generated by Django 4.0.1 on 2022-10-29 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_poll_delete_likepost_delete_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='image',
        ),
    ]
