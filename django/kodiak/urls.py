# project wide urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()
import settings
import django_databrowse

# App url imports.
import network.urls
import features.urls
import ontology_browser.urls
from chado.views import *


urlpatterns = patterns('',

    # Databrowse (For convenience)
    (r'^db/(.*)', django_databrowse.site.root),



    # app url includes:
    url(r'^', include(network.urls)),
    url(r'^', include(features.urls)),
    url(r'^', include(ontology_browser.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Home View
    url(r'/', 'kodiak.views.home'),
	#url(r'.*', 'kodiak.views.home'),


    # catch all, redirect to network home view
	#url(r'.*', RedirectView.as_view(url='/')),
)
