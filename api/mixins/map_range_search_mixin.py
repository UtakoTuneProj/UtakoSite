import json
from .base_map_search_mixin import BaseMapSearchMixIn

from .common import *

class MapRangeSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)

        if isvalid_range(get_request('range_start')) and isvalid_range(get_request('range_end')):
            context['range_start'] = json.loads(get_request('range_start'))
            context['range_end'] = json.loads(get_request('range_end'))
        else:
            raise ValidationError(detail='parameter "range_start" or "range_end" is not valid')

        return context

    def _get_queryset(self, objects, context):
        condition = {}
        for i in range(8):
            x = float( context['range_start'][i] )
            y = float( context['range_end'][i] )
            condition['songindex__value{}__range'.format(i)] = ( x, y )
        objects = objects.filter( **condition )

        return super()._get_queryset(objects, context)
