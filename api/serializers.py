from django.urls import path, include
from .models import Status, SongIndex, Chart
from rest_framework import serializers

# Serializers define the API representation.
class SongIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongIndex
        fields = ['values',] + ['value{}'.format(i) for i in range(8)]

class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        exclude = ('id', 'status')

class StatusSerializer(serializers.ModelSerializer):
    songindex_set = SongIndexSerializer(many=True)
    chart_set = ChartSerializer(many=True)

    class Meta:
        model = Status
        exclude = ('analyzegroup',)
