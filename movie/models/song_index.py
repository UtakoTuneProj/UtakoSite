
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .status import Status

class SongIndex(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.ForeignKey(Status, on_delete = models.CASCADE, max_length=12, default="UNKNOWN")  # Field name made lowercase.
    value0 = models.FloatField()
    value1 = models.FloatField()
    value2 = models.FloatField()
    value3 = models.FloatField()
    value4 = models.FloatField()
    value5 = models.FloatField()
    value6 = models.FloatField()
    value7 = models.FloatField()
    version = models.IntegerField()

    class Meta:
        db_table = 'song_index'
        unique_together = (('status', 'version'),)

