from django.urls import path

from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.detail_redirect, name='detail_redirect'),
    path('<str:movie_id>/', views.detail, name='detail'),
]
