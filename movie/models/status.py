# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Status(models.Model):
    pass

from django.db.models import Exists, OuterRef, Manager

class StatusManager(Manager):
    use_for_related_fields = True

    def analyzed(self, **kwargs):
        from .status_song_relation import StatusSongRelation
        ssr_subq = StatusSongRelation.objects.filter(status_id = OuterRef('id'))
        return Status.objects.annotate(_isanalyzed = Exists(ssr_subq)).filter(_isanalyzed = True, **kwargs)

class Status(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    validity = models.IntegerField()
    epoch = models.IntegerField()
    iscomplete = models.IntegerField(db_column='isComplete')  # Field name made lowercase.
    postdate = models.DateTimeField(blank=True, null=True)
    analyzegroup = models.IntegerField(db_column='analyzeGroup', blank=True, null=True)  # Field name made lowercase.

    @property
    def isanalyzed(self):
        from .status_song_relation import StatusSongRelation
        return StatusSongRelation.objects.filter(status_id = self.id).exists()

    objects = StatusManager()

    class Meta:
        db_table = 'status'

