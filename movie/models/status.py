# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Exists, OuterRef, Manager

class Status(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    validity = models.IntegerField()
    epoch = models.IntegerField()
    iscomplete = models.IntegerField(db_column='isComplete')  # Field name made lowercase.
    postdate = models.DateTimeField(blank=True, null=True)
    analyzegroup = models.IntegerField(db_column='analyzeGroup', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(blank=True, null=True)
    # 0: from raw, 1: forward estimate, -1: backword estimate
    score_status = models.IntegerField(blank=True, null=True)

    @property
    def isanalyzed(self):
        return self.statussongrelation_set.exists()

    class Meta:
        db_table = 'status'

