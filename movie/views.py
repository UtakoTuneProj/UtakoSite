from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count, F, Exists, OuterRef
from django.views.generic.list import ListView
from .models import Status, Chart, Idtag, Tagcolor, SongIndex, SongRelation, StatusSongRelation

# Create your views here.
class IndexView(ListView):
    model = Status
    template_name = 'movie/index.html'
    allow_empty = True
    paginate_by = 24
    ordering = '-postdate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_context_from_request(self.request))
        return context

    def get_context_from_request(self, request):
        get_request = request.GET.get
        context = {}
        if get_request('min_view') not in ['', None]:
            try:
                context['min_view'] = int(get_request('min_view'))
                if context['min_view'] < 0:
                    del context['min_view']
            except ValueError:
                pass

        if get_request('max_view') not in ['', None]:
            try:
                context['max_view'] = int(get_request('max_view'))
                if context['max_view'] < 0:
                    del context['max_view']
            except ValueError:
                pass

        if get_request('sortby') in ['', None]:
            context['sortby'] = self.ordering
        else:
            context['sortby'] = get_request('sortby')
            if context['sortby'] not in ['postdate', '-postdate', 'max_view', '-max_view']:
                raise ValueError
        self.ordering = context['sortby']

        if get_request('not_analyzed') == 'on':
            context['not_analyzed'] = True
        else:
            context['not_analyzed'] = False

        if get_request('perpage') not in ['', None]:
            paginate_by = get_request('perpage')

        return context

    def get_queryset(self):
        context = self.get_context_from_request(self.request)
        object_list = super().get_queryset()

        ssr_subq = StatusSongRelation.objects.filter(status_id = OuterRef('id'))
        movies_list = object_list.annotate(isanalyzed = Exists(ssr_subq))

        if not context['not_analyzed']:
            movies_list = movies_list.filter(isanalyzed = True)

        if hasattr(context, 'tags'):
            movies_list = movies_list.filter(
                idtag__tagname = context['tags']
            )

        if hasattr(context, 'min_view') \
            or hasattr(context, 'max_view') \
            or self.ordering in ['max_view', '-max_view']:
            movies_list = movies_list.annotate(
                max_view = Max('chart__view')
            )
        if hasattr(context, 'min_view'):
            movies_list = movies_list.filter(max_view__gt = context['min_view'])
        if hasattr(context, 'max_view'):
            movies_list = movies_list.filter(max_view__lt = context['max_view'])

        return movies_list.order_by(context['sortby'])

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
