from django.conf import settings
from .models import Status
from UtakoSite.mixins import StatusSearchMixIn
import json

class BaseMapSearchMixIn(StatusSearchMixIn):
    def get_context_from_request(self, request):
        get_request = getattr(request, request.method).get
        context = super().get_context_from_request(request)

        if get_request('version') and int(get_request('version')) in\
            range(settings.LATEST_ANALYZER_MODEL_VERSION + 1):
            context['version'] = int( get_request('version') )
        else:
            context['version'] = settings.LATEST_ANALYZER_MODEL_VERSION

        return context

    def _get_queryset(self, objects, context):
        objects = objects.filter(
            songindex__version=context["version"]
        )
        return super()._get_queryset(objects, context)

class MapRangeSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)

        def isvalid_range(txt):
            pos = json.loads(txt)
            if type(pos) not in (list, tuple):
                return False
            if len(pos) != 8:
                return False
            return True

        if isvalid_range(get_request('range_start')) and isvalid_range(get_request('range_end')):
            context['range_start'] = json.loads(get_request('range_start'))
            context['range_end'] = json.loads(get_request('range_end'))
        else:
            context['range_start'] = [-1,-1,-1,-1,-1,-1,-1,-1]
            context['range_end'] = [1,1,1,1,1,1,1,1]

        return context

    def _get_queryset(self, objects, context):
        condition = {}
        for i in range(8):
            x = float( context['range_start'][i] )
            y = float( context['range_end'][i] )
            condition['songindex__value{}__range'.format(i)] = ( x, y )
        objects = objects.filter( **condition )

        return super()._get_queryset(objects, context)

class MapPointSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        pass
    def _get_queryset(self, context):
        pass
