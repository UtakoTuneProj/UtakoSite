import json

from django.db.models import F, Func, FloatField, ExpressionWrapper
from django.db.models.functions import Now
from rest_framework.exceptions import ValidationError

from .base_map_search_mixin import BaseMapSearchMixIn
from .common import *

class Log10(Func):
    function='LOG'

class Sqrt(Func):
    function='SQRT'

class MapPointSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)

        if isvalid_range(get_request('origin')):
            context['origin'] = json.loads(get_request('origin'))
        else:
            raise ValidationError(detail='parameter "origin" is not valid')

        if get_request('score_factor') not in ['', None]:
            context['score_factor'] = float(get_request('score_factor')) / 10
        else:
            context['score_factor'] = float(0)

        if get_request('time_factor') not in ['', None]:
            context['time_factor'] = float(get_request('time_factor')) / 10
        else:
            context['time_factor'] = float(0)

        return context

    def _get_queryset(self, objects, context):
        condition = {}
        pos = context['origin']
        objects = objects.filter( **condition )
        objects = super()._get_queryset(objects, context)

        objects = objects.filter(
            score__isnull=False
        ).annotate(
            distance=Sqrt(( F('songindex__value0') - pos[0] ) ** 2
                + ( F('songindex__value1') - pos[1] ) ** 2
                + ( F('songindex__value2') - pos[2] ) ** 2
                + ( F('songindex__value3') - pos[3] ) ** 2
                + ( F('songindex__value4') - pos[4] ) ** 2
                + ( F('songindex__value5') - pos[5] ) ** 2
                + ( F('songindex__value6') - pos[6] ) ** 2
                + ( F('songindex__value7') - pos[7] ) ** 2
            ) - context['score_factor'] * Log10( F('score') + 1 )
            + context['time_factor'] * (
                Log10( ExpressionWrapper(
                    Now() - F('postdate'),
                    output_field=FloatField()
                )) - 11.0 ),
        ).order_by('distance')

        return objects
