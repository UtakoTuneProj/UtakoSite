from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tagname>/', views.detail, name='detail'),
]
