# Generated by Django 3.0.8 on 2020-07-12 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='racer',
            name='dropped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='racerround',
            name='dnf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='racerround',
            name='dropped',
            field=models.BooleanField(default=False),
        ),
    ]
