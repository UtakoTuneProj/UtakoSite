from django.conf import settings
from django.db.models import F
from .models import Status
from UtakoSite.mixins import StatusSearchMixIn
import json

def isvalid_range(txt):
    if txt is None:
        return False
    pos = json.loads(txt)
    if type(pos) not in (list, tuple):
        return False
    if len(pos) != 8:
        return False
    return True

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
        return super()._get_queryset(objects, context).prefetch_related('chart_set', 'songindex_set')

class MapRangeSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)

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
        get_request = request.GET.get
        context = super().get_context_from_request(request)

        if isvalid_range(get_request('origin')):
            context['origin'] = json.loads(get_request('origin'))
        else:
            context['origin'] = [0,0,0,0,0,0,0,0]

        return context

    def _get_queryset(self, objects, context):
        condition = {}
        pos = context['origin']
        objects = objects.filter( **condition )
        objects = super()._get_queryset(objects, context)

        objects = objects.annotate(
            distance=\
                ( F('songindex__value0') - pos[0] ) ** 2 \
                + ( F('songindex__value1') - pos[1] ) ** 2 \
                + ( F('songindex__value2') - pos[2] ) ** 2 \
                + ( F('songindex__value3') - pos[3] ) ** 2 \
                + ( F('songindex__value4') - pos[4] ) ** 2 \
                + ( F('songindex__value5') - pos[5] ) ** 2 \
                + ( F('songindex__value6') - pos[6] ) ** 2 \
                + ( F('songindex__value7') - pos[7] ) ** 2 \
        ).order_by('distance')

        return objects
