# Generated by Django 2.0.6 on 2018-06-04 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_analyzequeue_squashed_0006_auto_20180601_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('version', models.IntegerField()),
            ],
            options={
                'db_table': 'song_relation',
            },
        ),
        migrations.CreateModel(
            name='StatusSongRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.SongRelation')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Status')),
            ],
            options={
                'db_table': 'status_song_relation',
            },
        ),
    ]