from django.shortcuts import render
from .models import Status
from .serializers import StatusSerializer
from rest_framework import generics, mixins
from UtakoSite.mixins import StatusSearchMixIn
from .mixins import MapRangeSearchMixIn, MapPointSearchMixIn
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# ViewSets define the view behavior.
class StatusList(generics.ListAPIView, StatusSearchMixIn):
    serializer_class = StatusSerializer

    def get_queryset(self):
        objects = Status.objects
        context = super().get_context_from_request(self.request)
        return self._get_queryset(objects, context).prefetch_related('chart_set', 'songindex_set')

class StatusRetrieve(generics.RetrieveAPIView):
    queryset = Status.objects
    serializer_class = StatusSerializer

class MapRangeList(generics.GenericAPIView, mixins.ListModelMixin, MapRangeSearchMixIn):
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        objects = Status.objects
        context = self.get_context_from_request(self.request)
        return self._get_queryset(objects, context)

class MapPointList(generics.GenericAPIView, mixins.ListModelMixin, MapPointSearchMixIn):
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        objects = Status.objects
        context = self.get_context_from_request(self.request)
        return self._get_queryset(objects, context)
