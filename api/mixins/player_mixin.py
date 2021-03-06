import json
import random
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from django.conf import settings
from django.http import Http404
import numpy as np
from numpy import linalg

from .base_map_search_mixin import BaseMapSearchMixIn
from .common import *
from ..models import Status, SongIndex
import api.views

TAG_BLACKLIST = {
    'ボカロカラオケDB',
    'ニコカラ',
    '歌ってみた',
    'ニコニコカラオケDB',
    'VOCALOIDランキング',
    '演奏してみた',
    '日刊VOCALOIDランキング',
    '日刊トップテン！VOCALOID＆something',
    'VOCALOIDメドレー',
    'XFD',
    'クロスフェードデモ',
    'VOCALOID-CDデモ',
    '例のアレ',
    '紳士向け'
}
POSITION_STEP = 0.1
VERSION = settings.LATEST_ANALYZER_MODEL_VERSION

class PlayerMixIn(BaseMapSearchMixIn):
    decode_nparray = lambda _, p: '[' + ','.join(map(lambda x: '{:.3}'.format(x), p)) + ']'

    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = super().get_context_from_request(request)

        if get_request('origin_id'):
            context['origin_id'] = get_request('origin_id')
            request.session['played'] = []
        context['played'] = request.session['played'] if 'played' in request.session else []

        self.session = request.session

        return context

    def _get_queryset(self, objects, context):
        if 'origin_id' in context:
            next_id = context['origin_id']
        else:
            next_id = self.search_next_song(context)

        self.session['played'] = context['played'] + [next_id]

        try:
            return Status.objects.filter(pk=next_id)
        except Status.DoesNotExist:
            raise Http404("selected movie {} is not tracked".format(next_id))

    def search_next_song(self, context, page=1):
        pos = self.get_nextpos(context)
        results = api.views.MapPointList()._get_queryset(
            objects = Status.objects,
            context = {
                'origin': pos,
                'version': VERSION,
                'not_analyzed': False,
                'sortby': 'distance',
                'time_factor': context['time_factor'],
                'score_factor': context['score_factor'],
            }
        )[(page-1)*5:page*5]

        for result in results:
            next_id = result.id
            if self.is_playable(next_id, context):
                break
        else:
            next_id = self.search_next_song(context, page + 1)

        return next_id

    def get_nextpos(self, context):
        previous_position = np.array( SongIndex.objects.get(
            status=context['played'][-1],
            version=VERSION
        ).values )\
        if len( context['played'] ) > 0\
        else np.array([random.random() * 2 - 1 for i in range(8)])

        vec = previous_position - np.array( SongIndex.objects.get(
            status=context['played'][-2],
            version=VERSION
        ).values )\
        if len( context['played'] ) > 1\
        else np.random.randn(8)

        vec = vec / linalg.norm(vec)
        return previous_position + POSITION_STEP * np.random.normal(1, 0.25) * vec

    def is_playable(self, mvid, context):
        if mvid in context['played']:
            return False

        req = Request('http://ext.nicovideo.jp/api/getthumbinfo/{}'.format(mvid))
        with urlopen(req) as response:
            root = ElementTree.fromstring(response.read())

        if not root.get('status') == 'ok':
            return False

        if root.find('../.embeddable') == 0:
            return False

        tags = set(x.text for x in root.findall('.//tag'))

        if not tags.isdisjoint( TAG_BLACKLIST ):
            return False
        if 'VOCALOID' not in tags:
            return False

        return True
