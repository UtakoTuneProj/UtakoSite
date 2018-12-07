from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import StatusList, StatusRetrieve, MapRangeList, MapPointList, PlayerList
from rest_framework import routers

urlpatterns = [
    path('movie/', StatusList.as_view()),
    path('movie/<str:pk>/', StatusRetrieve.as_view(), name='detail'),
    path('vocalosphere/range/', MapRangeList.as_view()),
    path('vocalosphere/point/', MapPointList.as_view()),
    path('player/', PlayerList.as_view()),
]
