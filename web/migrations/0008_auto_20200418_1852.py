# Generated by Django 3.0.5 on 2020-04-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='publication',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]