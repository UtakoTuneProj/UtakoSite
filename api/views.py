from django.shortcuts import render
from .models import Status
from .serializers import StatusSerializer
from rest_framework import generics
from movie.views import MovieIndexMixIn

# Create your views here.

# ViewSets define the view behavior.
class StatusList(generics.ListAPIView, MovieIndexMixIn):
    serializer_class = StatusSerializer

    def get_queryset(self):
        objects = Status.objects
        context = self.get_context_from_request(self.request)
        return self._get_queryset(objects, context).prefetch_related('chart_set')

class StatusRetrieve(generics.RetrieveAPIView):
    queryset = Status.objects
    serializer_class = StatusSerializer
