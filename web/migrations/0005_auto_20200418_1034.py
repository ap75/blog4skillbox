# Generated by Django 3.0.5 on 2020-04-18 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20200415_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]