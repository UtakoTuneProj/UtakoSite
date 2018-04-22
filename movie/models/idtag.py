# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .status import Status

class Idtag(models.Model):
    id = models.ForeignKey(Status, on_delete=models.CASCADE, db_column='ID', primary_key = True, max_length=12)  # Field name made lowercase.
    tagname = models.CharField(db_column='tagName', max_length=60)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'IDtag'
        unique_together = (('id', 'tagname'),)

