# Generated by Django 3.0.5 on 2020-04-15 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20200415_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='author',
        ),
    ]