from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from xml.etree import ElementTree
from datetime import datetime as dt
import json
import asyncio
import copy

from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import F
from django.views.generic.list import ListView

from .models import Status, Chart, Idtag, Tagcolor, SongIndex, SongRelation, StatusSongRelation
from UtakoSite.mixins import StatusSearchMixIn

NICOAPI_KWARGS = {
    'q',
    'targets',
    'filters',
    'jsonFilter',
    '_sort',
}
MINIMUM_KWARGS = {
    'q',
    'targets',
    '_sort'
}

NICOAPI_BASE = "https://api.search.nicovideo.jp/api/v2/video/contents/search?"

def parse_nicoapi(movie_id):
    def no_response():
        return {
            'title': 'NOT FOUND',
            'thumbnail_url': None,
            'view_counter': '---',
            'mylist_counter': '---',
            'comment_num': '---',
            'user_nickname': '---',
            'first_retrieve': '---',
        }

    ret = {}
    req = Request(
        "http://ext.nicovideo.jp/api/getthumbinfo/" + movie_id
    )
    try:
        with urlopen(req) as response:
            root = ElementTree.fromstring(response.read())
    except HTTPError:
        ret.update(no_response())
    else:
        if root.get('status') == 'ok':
            for child in root[0]:
                if child.tag == 'tags':
                    ret['tags'] = [x.text for x in child]
                elif child.tag in [
                    "mylist_counter",
                    "comment_num",
                    "view_counter"
                ]:
                    ret[child.tag] = int(child.text)
                elif child.tag == 'first_retrieve':
                    ret[child.tag] = dt.strptime(child.text, '%Y-%m-%dT%H:%M:%S+09:00')
                else:
                    ret[child.tag] = child.text
        else:
            ret.update(no_response())

    return ret

class MovieIndexMixIn(StatusSearchMixIn):
    async def get_nicoapi(self, **kwargs):
        uri = NICOAPI_BASE + urlencode(kwargs)
        req = Request(uri)
        with urlopen(req) as _:
            nicoapi_result = json.loads(_.read().decode())
        return [m['contentId'] for m in nicoapi_result["data"]]

    async def get_nicoapis(self, result_count, **kwargs):
        pages = min(result_count, 1600) // kwargs['_limit'] + 1
        api_kwargs = []
        for i in range(pages):
            api_kwargs.append(copy.deepcopy(kwargs))
            api_kwargs[-1]['_offset'] = kwargs['_limit'] * i
        results = await asyncio.gather(*[self.get_nicoapi(**k) for k in api_kwargs])
        return sum(results, [])

    def unify_nico_search_api(self, context):
        nico_api = context['nico_api']
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        minimum_search = {}
        for k in MINIMUM_KWARGS:
            minimum_search[k] = nico_api[k]
        uri = NICOAPI_BASE + urlencode(minimum_search)
        req = Request(uri)
        with urlopen(req) as _:
            result_count = json.loads(_.read().decode())['meta']['totalCount']

        return loop.run_until_complete(self.get_nicoapis(result_count, **nico_api))

    def _get_queryset(self, objects, context):
        if context['nico_api']['q'] not in ['', None]:
            filter_list = self.unify_nico_search_api(context)
            objects = objects.filter(id__in = filter_list)

        return super()._get_queryset(objects, context).prefetch_related('statussongrelation_set')

    def get_context_from_request(self, request):
        get_request = getattr(request, request.method).get
        context = super().get_context_from_request(request)
        context['nico_api'] = {
            'q': None,
            'targets': 'tags',
            'fields': 'contentId',
            '_sort': '-startTime',
            '_context': 'https://utako-tune.jp/',
            '_limit': 100
        }
        for keyword in NICOAPI_KWARGS:
            if get_request(keyword) not in ['', None]:
                context['nico_api'][keyword] = get_request(keyword)

        return context

# Create your views here.
class IndexView(ListView, MovieIndexMixIn):
    model = Status
    template_name = 'movie/index.html'
    allow_empty = True
    paginate_by = 24

    def refer_from_nicoapi(self, page_obj):
        context = {'card_content': []}
        for movie in page_obj:
            ret = parse_nicoapi(movie.id)
            ret['movie'] = movie
            context['card_content'].append(ret)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(super().get_context_from_request(self.request))
        context.update(self.refer_from_nicoapi(context['page_obj']))
        return context

    def get_queryset(self):
        context = super().get_context_from_request(self.request)
        objects = Status.objects

        return super()._get_queryset(objects, context)

def detail(request, movie_id):
    movie = get_object_or_404(Status, id = movie_id)
    chart = Chart.objects.filter(status_id = movie_id)
    tags = Idtag.objects.filter(status_id = movie_id)
    song_index = Status.objects.get(pk=movie_id).songindex_set.all()
    related = StatusSongRelation.objects.filter(
        status_id = movie_id
    ).prefetch_related(
        'song_relation__id__status_song_relation'
    ).annotate(
        destination = F('song_relation__statussongrelation__status_id')
    ).exclude(
        destination = movie_id
    ).order_by('song_relation__distance')[:12]

    card_content = []
    for rel_movie in related:
        ret = parse_nicoapi(rel_movie.destination)
        ret['movie'] = Status.objects.get(id=rel_movie.destination)
        card_content.append(ret)

    return render( request, 'movie/detail.html', {
        'movie': movie,
        'chart': chart,
        'tags': tags,
        'related': related,
        'card_content': card_content,
        'song_index': song_index,
    })

def detail_redirect(request):
    movie_id = request.GET.get('movie_id')
    return redirect('/movie/{}'.format(movie_id))
