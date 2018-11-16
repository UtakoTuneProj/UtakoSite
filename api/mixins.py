from django.conf import settings
from .models import Status
from UtakoSite.mixins import StatusSearchMixIn

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
        request_query = getattr(request, request.method)
        get_request = request_query.get
        getlist = getattr(request, request.method).getlist
        context = super().get_context_from_request(request)

        if 'range_start' in request_query and 'range_end' in request_query:
            context['range_start'] = getlist('range_start')
            context['range_end'] = getlist('range_end')
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
