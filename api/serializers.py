from django.urls import path, include
from .models import Status, SongIndex
from rest_framework import serializers

# Serializers define the API representation.
class SongIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongIndex
        fields = ('value0', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'version')

class StatusSerializer(serializers.ModelSerializer):
    song_index = SongIndexSerializer(many=True)

    class Meta:
        model = Status
        fields = ('id', 'epoch', 'isanalyzed', 'song_index')
