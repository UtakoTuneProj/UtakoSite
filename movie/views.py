from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count
from .models import Status, Chart, Idtag, Tagcolor

# Create your views here.
def index(request):
    page = request.GET.get('page')
    perpage = request.GET.get('perpage', default = 24)
    sortby = request.GET.get('sortby', default = '-postdate')
    tags = request.GET.get('tags')
    validity = request.GET.get('validity', default = -1)
    iscomplete = request.GET.get('iscomplete', default = -1)
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
    
    movies_list = Status.objects.all()

    if validity in ['0','1']:
        movies_list = movies_list.filter(validity = validity)
    if iscomplete in ['0','1']:
        movies_list = movies_list.filter(iscomplete = iscomplete)

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

    paginator = Paginator(movies_list, perpage)
    movies = paginator.get_page(page)
    return render(request, 'movie/index.html', {
        'movies': movies,
        'page': movies,
        'tags': tags if tags is not None else '',
        'max_view': max_view if max_view > 0 else '',
        'min_view': min_view if min_view > 0 else '',
    })

def detail(request, movie_id):
    movie = get_object_or_404(Status, id=movie_id)
    chart = Chart.objects.filter(id=movie_id)
    tags = Idtag.objects.filter(id=movie_id)
    return render(request, 'movie/detail.html', { 'movie': movie, 'chart': chart, 'tags': tags })
