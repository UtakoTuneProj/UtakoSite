from django.db import models

class SongRelation(models.Model):
    distance = models.IntegerField()
    version = models.IntegerField()

    class Meta:
        db_table = 'song_relation'

