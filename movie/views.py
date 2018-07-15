from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count, F, Exists, OuterRef
from .models import Status, Chart, Idtag, Tagcolor, SongIndex, SongRelation, StatusSongRelation

# Create your views here.
def index(request):
    page = request.GET.get('page', default=1)
    perpage = request.GET.get('perpage', default = 24)
    sortby = request.GET.get('sortby', default = '-postdate')
    tags = request.GET.get('tags')
    isanalyzed = request.GET.get('isanalyzed', default = 'on')
    min_view = request.GET.get('min_view', default = -1)
    max_view = request.GET.get('max_view', default = -1)

    if min_view not in ('', None):
        min_view = int(min_view)
    else:
        min_view = -1
    if max_view not in ('', None):
        max_view = int(max_view)
    else:
        max_view = -1
    if sortby not in ['postdate', '-postdate', 'max_view', '-max_view']:
        sortby = '-postdate'

    ssr_subq = StatusSongRelation.objects.filter(status_id = OuterRef('id'))
    movies_list = Status.objects.annotate(isanalyzed = Exists(ssr_subq))

    if isanalyzed == 'on':
        movies_list = movies_list.filter(isanalyzed = True)

    if tags not in ( '', None ):
        movies_list = movies_list.filter(
            idtag__tagname = tags
        )

    if min_view >= 0 or max_view >= 0 or sortby == 'max_view' or sortby == '-max_view':
        movies_list = movies_list.annotate(
            max_view = Max('chart__view')
        )
    if min_view >= 0:
        movies_list = movies_list.filter(max_view__gt = min_view)
    if max_view >= 0:
        movies_list = movies_list.filter(max_view__lt = max_view)

    movies_list = movies_list.order_by(sortby)

    movies = Paginator(movies_list, perpage).get_page(page)
    return render(request, 'movie/index.html', {
        'movies': movies,
        'page': movies,
        'tags': tags if tags is not None else '',
        'max_view': max_view if max_view > 0 else '',
        'min_view': min_view if min_view > 0 else '',
        'isanalyzed': True if isanalyzed == 'on' else False,
        'sortby': sortby
    })

def detail(request, movie_id):
    movie = get_object_or_404(Status, id = movie_id)
    chart = Chart.objects.filter(id = movie_id)
    tags = Idtag.objects.filter(id = movie_id)
    related = StatusSongRelation.objects.filter(
        status_id = movie_id
    ).prefetch_related(
        'song_relation__id__status_song_relation'
    ).annotate(
        destination = F('song_relation__statussongrelation__status_id')
    ).exclude(
        destination = movie_id
        ).order_by('song_relation__distance')[:12]
    return render( request, 'movie/detail.html', {
        'movie': movie,
        'chart': chart,
        'tags': tags,
        'related': related,
    })

def detail_redirect(request):
    movie_id = request.GET.get('movie_id')
    print(movie_id)
    return redirect('/movie/{}'.format(movie_id))
