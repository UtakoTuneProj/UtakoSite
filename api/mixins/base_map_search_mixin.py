from django.conf import settings
from UtakoSite.mixins import StatusSearchMixIn

class BaseMapSearchMixIn(StatusSearchMixIn):
    def get_context_from_request(self, request):
        get_request = getattr(request, request.method).get
        context = super().get_context_from_request(request)

        if get_request('version') and int(get_request('version')) in\
            range(settings.LATEST_ANALYZER_MODEL_VERSION + 1):
            context['version'] = int( get_request('version') )
        else:
            context['version'] = settings.LATEST_ANALYZER_MODEL_VERSION

        if get_request('score_factor') not in ['', None]:
            context['score_factor'] = float(get_request('score_factor')) / 10
        else:
            context['score_factor'] = float(0)

        if get_request('time_factor') not in ['', None]:
            context['time_factor'] = float(get_request('time_factor')) / 10
        else:
            context['time_factor'] = float(0)

        return context

    def _get_queryset(self, objects, context):
        objects = objects.filter(
            songindex__version=context["version"]
        )
        return super()._get_queryset(objects, context).prefetch_related('songindex_set')
