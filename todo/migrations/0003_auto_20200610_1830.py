# Generated by Django 3.0.7 on 2020-06-10 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20200610_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='user_id',
            new_name='user',
        ),
    ]
