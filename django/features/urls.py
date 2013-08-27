# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'^features/$', 'features.views.search_features', name="search_features"),
)
