"""UtakoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.flatpages import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movie.urls')),
    path('tag/', include('tag.urls')),
    path('auth/', include('register.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('', include('django.contrib.auth.urls')),
    re_path('^$', views.flatpage, {'url': 'index/'})
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path('^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
