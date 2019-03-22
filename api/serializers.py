from django.urls import path, include
from .models import Status, SongIndex, Chart
from rest_framework import serializers

# Serializers define the API representation.
class SongIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongIndex
        fields = ['values',] + ['value{}'.format(i) for i in range(8)]

class StatusSerializer(serializers.ModelSerializer):
    songindex_set = SongIndexSerializer(many=True)

    class Meta:
        model = Status
        exclude = ('analyzegroup',)
