from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Status, Chart, Idtag, Tagcolor

# Create your views here.
def index(request):
    page = request.GET.get('page')
    perpage = request.GET.get('perpage', default = 24)
    sortby = request.GET.get('sortby', default = '-postdate')
    if sortby not in ['postdate', '-postdate']:
        sortby = '-postdate'
    validity = request.GET.get('validity', default = -1)
    iscomplete = request.GET.get('iscomplete', default = -1)
    min_view = request.GET.get('min_view', default = 0)
    max_view = request.GET.get('max_view', default = -1)
    
    movies_list = Status.objects.all().order_by(sortby)

    if validity in ['0','1']:
        movies_list = movies_list.filter(validity = validity)
    if iscomplete in ['0','1']:
        movies_list = movies_list.filter(iscomplete = iscomplete)

    paginator = Paginator(movies_list, perpage)
    movies = paginator.get_page(page)
    return render(request, 'movie/index.html', {'movies': movies, 'page': movies})

def detail(request, movie_id):
    movie = get_object_or_404(Status, id=movie_id)
    chart = Chart.objects.filter(id=movie_id)
    tags = Idtag.objects.filter(id=movie_id)
    return render(request, 'movie/detail.html', { 'movie': movie, 'chart': chart, 'tags': tags })
