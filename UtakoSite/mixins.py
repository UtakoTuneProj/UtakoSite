from django.db.models import Max

class StatusSearchMixIn():
    def _get_queryset(self, objects, context):

        if not context['not_analyzed']:
            objects = objects.filter(songindex__isnull = False)
        if 'tags' in context:
            objects = objects.filter(
                idtag__tagname = context['tags']
            )

        if 'min_view' in context\
            or 'max_view' in context \
            or context['sortby'] in ['max_view', '-max_view']:
            objects = objects.annotate(
                max_view = Max('chart__view')
            )
        if 'min_view' in context:
            objects = objects.filter(max_view__gte = context['min_view'])
        if 'max_view' in context:
            objects = objects.filter(max_view__lte = context['max_view'])

        return objects.order_by(context['sortby'])

    def get_context_from_request(self, request):
        get_request = getattr(request, request.method).get
        context = {}
        ordering = '-postdate'
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

        if get_request('sortby') in [
            'postdate',
            '-postdate',
            'max_view',
            '-max_view'
        ]:
            context['sortby'] = get_request('sortby')
        else:
            context['sortby'] = ordering

        if get_request('not_analyzed') in ( '1', 'on' ):
            context['not_analyzed'] = True
        else:
            context['not_analyzed'] = False

        if get_request('tags') not in ['', None]:
            context['tags'] = get_request('tags')

        if get_request('perpage') not in ['', None]:
            self.paginate_by = get_request('perpage')

        return context

