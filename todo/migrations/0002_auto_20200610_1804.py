# Generated by Django 3.0.7 on 2020-06-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='dt_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]