from django.shortcuts import render
from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework import generics, mixins, views, response

from UtakoSite.mixins import StatusSearchMixIn
from .models import Status
from .serializers import StatusSerializer
from .mixins import MapRangeSearchMixIn, MapPointSearchMixIn, PlayerMixIn
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

class BaseUtakoList(generics.GenericAPIView):
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        objects = Status.objects
        context = self.get_context_from_request(self.request)
        return self._get_queryset(objects, context)

class MapRangeList(BaseUtakoList, mixins.ListModelMixin, MapRangeSearchMixIn):
    pass

class MapPointList(BaseUtakoList, mixins.ListModelMixin, MapPointSearchMixIn):
    pass

class PlayerList(BaseUtakoList, mixins.ListModelMixin, PlayerMixIn):
    pass

class SettingsRetrieve(views.APIView):
    def get(self, request):
        return response.Response( request.session )
    def put(self, request):
        request.session = request.data
        return response.Response( request.session )
    def patch(self, request):
        for key in request.data.keys():
            request.session[key] = request.data[key]
        return response.Response( request.session )
