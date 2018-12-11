import json
import random
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from django.conf import settings
import numpy as np
from numpy import linalg

from .base_map_search_mixin import BaseMapSearchMixIn
from .common import *
from ..models import Status, SongIndex
import api.views

TAG_BLACKLIST = {
    'MikuMikuDance',
    'MMD',
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
    'クロスフェードデモ'
}
POSITION_STEP = 0.03
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

        return Status.objects.filter(pk=next_id)

    def search_next_song(self, context, page=1):
        pos = self.get_nextpos(context)
        results = api.views.MapPointList()._get_queryset(
            objects = Status.objects,
            context = {
                'origin': pos,
                'version': VERSION,
                'not_analyzed': False,
                'sortby': 'distance',
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
        tree = {}

        if mvid in context['played']:
            return False

        req = Request('http://ext.nicovideo.jp/api/getthumbinfo/{}'.format(mvid))
        with urlopen(req) as response:
            root = ElementTree.fromstring(response.read())

        if root.get('status') == 'ok':
            for child in root[0]:
                if child.tag == 'tags':
                    tree['tags'] = set(x.text for x in child)
        else:
            return False

        if not tree['tags'].isdisjoint( TAG_BLACKLIST ):
            return False

        return True
