from django.conf import settings

def google_ad_client(request):
    return {'google_ad_client': settings.GOOGLE_AD_CLIENT}
