from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import StatusList, StatusRetrieve, MapRangeList, MapPointList
from rest_framework import routers

urlpatterns = [
    path('movie/', StatusList.as_view()),
    path('movie/<str:pk>/', StatusRetrieve.as_view(), name='detail'),
    path('vocalosphere/range/', MapRangeList.as_view()),
]
