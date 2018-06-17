# Generated by Django 2.0.6 on 2018-06-17 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('movie', '0007_auto_20180617_0135'), ('movie', '0008_auto_20180617_1234'), ('movie', '0009_auto_20180617_1243')]

    dependencies = [
        ('movie', '0006_songrelation_statussongrelation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='id',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='chart',
            name='status',
            field=models.ForeignKey(default='UNKNOWN', max_length=12, on_delete=django.db.models.deletion.CASCADE, to='movie.Status'),
        ),
        migrations.AddField(
            model_name='chart',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together={('status', 'epoch')},
        ),
        migrations.RenameField(
            model_name='idtag',
            old_name='id',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='idtag',
            name='status',
            field=models.ForeignKey(db_column='status_id', default='UNKNOWN', max_length=12, on_delete=django.db.models.deletion.CASCADE, to='movie.Status'),
        ),
        migrations.AddField(
            model_name='idtag',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='idtag',
            unique_together={('status', 'tagname')},
        ),
        migrations.RenameField(
            model_name='songindex',
            old_name='id',
            new_name='status',
        ),
        migrations.AddField(
            model_name='songindex',
            name='status',
            field=models.ForeignKey(default='UNKNOWN', max_length=12, on_delete=django.db.models.deletion.CASCADE, to='movie.Status'),
        ),
        migrations.AddField(
            model_name='songindex',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='songindex',
            unique_together={('status', 'version')},
        ),
    ]
