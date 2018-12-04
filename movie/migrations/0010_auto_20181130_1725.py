# Generated by Django 2.0.6 on 2018-11-30 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0009_auto_20181115_0025'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value0'], name='song_index_value0_390586_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value1'], name='song_index_value1_b5f5ab_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value2'], name='song_index_value2_10cbcd_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value3'], name='song_index_value3_b6a7e9_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value4'], name='song_index_value4_447dfc_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value5'], name='song_index_value5_cbb14b_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value6'], name='song_index_value6_835a3f_idx'),
        ),
        migrations.AddIndex(
            model_name='songindex',
            index=models.Index(fields=['value7'], name='song_index_value7_8fa359_idx'),
        ),
    ]
