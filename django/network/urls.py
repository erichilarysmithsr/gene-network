# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',

    url(r'^network/$', 'network.views.show_network', name="network"),

    # typeahead view
    url(r'^t/$', 'network.views.search', name='cvterm_search'),
)
