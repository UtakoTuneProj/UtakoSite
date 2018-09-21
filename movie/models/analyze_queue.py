
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .status import Status

class AnalyzeQueue(models.Model):
    movie_id = models.ForeignKey(Status, on_delete = models.CASCADE, db_column='movie_id', max_length=12)  # Field name made lowercase.
    version = models.IntegerField()
    status = models.IntegerField()
    queued_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analyze_queue'
