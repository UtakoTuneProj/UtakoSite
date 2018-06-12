from django.conf import settings

def isdebug(request):
    return {'isdebug': settings.DEBUG}
