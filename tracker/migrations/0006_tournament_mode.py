# Generated by Django 3.0.8 on 2020-10-06 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_racerround_position_in_round'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='mode',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Normal'), (2, 'PB')], default=1),
        ),
    ]