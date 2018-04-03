from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Status, Chart, Idtag, Tagcolor
from django.db.models import Count

# Create your views here.
def index(request):
    tags_list = Idtag.objects.values('tagname').annotate(cnt = Count('tagname')).order_by('-cnt')
    paginator = Paginator(tags_list, 100)

    page = request.GET.get('page')
    tags = paginator.get_page(page)
    return render(request, 'tag/index.html', {'tags': tags, 'tags_list': tags_list, 'page': tags})

def detail(request, tagname):
    movies_list = get_list_or_404(Idtag, tagname=tagname)
    paginator = Paginator(movies_list, 10)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'tag/detail.html', { 'tagname': tagname, 'movies': movies, 'page': movies})
