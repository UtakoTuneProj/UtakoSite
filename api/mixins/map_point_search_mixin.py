import json

from django.db.models import F
from rest_framework.exceptions import ValidationError

from .base_map_search_mixin import BaseMapSearchMixIn
from .common import *

class MapPointSearchMixIn(BaseMapSearchMixIn):
    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)
        print(get_request('origin'))

        if isvalid_range(get_request('origin')):
            context['origin'] = json.loads(get_request('origin'))
        else:
            raise ValidationError(detail='parameter "origin" is not valid')

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
