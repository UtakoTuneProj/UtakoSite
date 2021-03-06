# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .status import Status

class Chart(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, max_length=12, default='UNKNOWN')  # Field name made lowercase.
    epoch = models.IntegerField()
    time = models.FloatField(db_column='Time')  # Field name made lowercase.
    view = models.IntegerField(db_column='View')  # Field name made lowercase.
    comment = models.IntegerField(db_column='Comment')  # Field name made lowercase.
    mylist = models.IntegerField(db_column='Mylist')  # Field name made lowercase.

    class Meta:
        db_table = 'chart'
        unique_together = (('status', 'epoch'),)
        indexes = [
            models.Index(fields=['view',]),
            models.Index(fields=['status','view']),
        ]
