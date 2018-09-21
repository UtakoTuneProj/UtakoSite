from django.db import models
from .status import Status
from .song_relation import SongRelation

class StatusSongRelation(models.Model):
    status = models.ForeignKey(Status, on_delete = models.CASCADE)
    song_relation = models.ForeignKey(SongRelation, on_delete = models.CASCADE)

    class Meta:
        db_table = 'status_song_relation'
