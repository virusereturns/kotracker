# Generated by Django 3.0.8 on 2020-07-12 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Racer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('pb', models.TimeField(blank=True, null=True)),
                ('eliminated', models.BooleanField(default=False)),
                ('position', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('best_time_in_race', models.TimeField(blank=True, null=True)),
                ('average_time_in_race', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('date', models.DateField(blank=True, null=True)),
                ('game', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Tournament')),
            ],
        ),
        migrations.CreateModel(
            name='RacerRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, null=True)),
                ('eliminated', models.BooleanField(default=False)),
                ('racer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Racer')),
                ('round_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Round')),
            ],
        ),
        migrations.AddField(
            model_name='racer',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Tournament'),
        ),
    ]
