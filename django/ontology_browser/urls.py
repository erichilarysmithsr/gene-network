from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
	# Ontology Browser
    url(r'^browser/$', 'ontology_browser.views.browser',name="browser"),
    url(r'^browser/tree_req/(?P<cvterm_id>[0-9]{1,20})?', 'ontology_browser.views.tree_req', name='tree_req'),

)
