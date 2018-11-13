from django.shortcuts import render
from .models import Status
from .serializers import StatusSerializer
from rest_framework import viewsets

# Create your views here.

# ViewSets define the view behavior.
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.analyzed()
    serializer_class = StatusSerializer
