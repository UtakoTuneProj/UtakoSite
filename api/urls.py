from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import StatusViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('statuses', StatusViewSet)

urlpatterns = [
    path('', include(router.urls))
]
