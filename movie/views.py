from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Status, Chart, Idtag, Tagcolor

# Create your views here.
def index(request):
    movies_list = Status.objects.all().order_by('postdate')
    paginator = Paginator(movies_list, 10)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movie/index.html', {'movies': movies, 'page': movies})

def detail(request, movie_id):
    movie = get_object_or_404(Status, id=movie_id)
    chart = Chart.objects.filter(id=movie_id)
    tags = Idtag.objects.filter(id=movie_id)
    return render(request, 'movie/detail.html', { 'movie': movie, 'chart': chart, 'tags': tags })
