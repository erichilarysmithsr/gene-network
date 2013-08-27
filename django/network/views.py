from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import urllib2
import ast
from chado.models import *
import re
from django import db  
from django.db.models import Q

def cvterm_cvterm_rel(node,blacklist):
    # Fetch Phenotypes
    phenotypes = list(node.cvterm_relationship_subject.select_related().filter(
        type__name='has_symptom',
        object__cv__name='human_phenotype'
        ).exclude(object__cvterm_id__in=blacklist).values_list(
        'subject__cvterm_id', # [0]
        'object__cvterm_id',  # [1]
        'subject__name',      # [2]
        'object__name',       # [3]
        'subject__cv__name',  # [4]
        'object__cv__name',   # [5]
        'type__name',         # [6]
        )[0:2])
    # Fetch Diseases
    diseases = list(node.cvterm_relationship_object.select_related().filter(
        type__name='has_symptom',
        subject__cv__name='disease_ontology'
        ).exclude(subject__cvterm_id__in=blacklist).values_list(
        'subject__cvterm_id',
        'object__cvterm_id',
        'subject__name',
        'object__name',
        'subject__cv__name',
        'object__cv__name',
        'type__name',
        )[0:2])

    return phenotypes + diseases


""" You are entering a set of confusing functions and swaps! It's easy to confuse! """
def feature_cvterm_rel(node):
    gene_disease = list(node.fc_cvterm_set.all().prefetch_related().values_list(
        'feature__feature_id',
        'cvterm__cvterm_id',
        'feature__name',
        'cvterm__name',
        'feature__type__name',
        'cvterm__cv__name',
        'feature__type__name',
        'cvterm__cv__name',
        ))
    return gene_disease

def cvterm_feature_rel(node):
    # Only triggered for cv terms!
    gene_disease = list(node.fc_feature_set.all().prefetch_related().values_list(
        'cvterm__cvterm_id',
        'feature__feature_id',
        'cvterm__name',
        'feature__name',
        'cvterm__cv__name',
        'feature__type__name',
        ))[0:8]
    return gene_disease


def draw_network(node, node_type, depth = 3, EDGES = [],blacklist=[]):
    """ This network takes an object, determines its type, and finds edges. """
    
    if depth > 0:
        # Fetch Edges
        f = vars(node)
        NEW_EDGES = []
        if node_type == "cvterm":
            # FETCH cvterm-cvterm relations!
            NEW_EDGES = [x + (depth,'cvterm',) for x in cvterm_cvterm_rel(node,blacklist)]
            # Fetch Related Features
            NEW_EDGES += [x + (depth,'feature',) for x in cvterm_feature_rel(node)]
        elif node_type == "feature":
            # Fetch Related CvTerms
            NEW_EDGES = [x + (depth,'cvterm',) for x in feature_cvterm_rel(node)]

        # Pull out cvterm nodes:
        for edge in NEW_EDGES:
            if edge[-1] == 'cvterm':
                # Blacklist prevents quieries from capturing previous terms.
                blacklist += [x[0] for x in NEW_EDGES] + [x[1] for x in NEW_EDGES]
                #blacklist = []
                node1 = Cvterm.objects.select_related().get(pk=edge[0])
                node2 = Cvterm.objects.prefetch_related().get(pk=edge[1])
                EDGES += draw_network(node1, edge[-1], depth-1, blacklist=blacklist)
                EDGES += draw_network(node2, edge[-1], depth-1, blacklist=blacklist)


        f = vars(node)
        #asdf
        EDGES += set(NEW_EDGES) 

    return set(EDGES)



def show_network(request):
    EDGES = "" # Not sure why - but EDGES is caching apparently...
    # NEED TO CLEAN UP..>A LOT!

    # Flag for loading cytoscape.js; For debugging purposes.
    load_cytoscape = True

    # Retrieve search term and set title.
    if 'q' in request.POST:
        try:
            search_term = Cvterm.objects.select_related().get(name=request.POST['q'])
            node_type = "cvterm"
        except ObjectDoesNotExist:
            search_term = Feature.objects.get(name=request.POST['q'])
            node_type = "feature"
        TITLE = search_term.name
    else:
        search_term = Cvterm.objects.select_related().get(name='cleft palate')
        node_type = "cvterm"

    # Edges Format:
    # [0] - target
    #

    EDGES = draw_network(search_term, node_type, 2)

    # Nodes Formatted as follows:
    # [0] - cvterm_id
    # [1] - Name
    # [2]
    NODES = [(x[0],x[2],x[4],x[7]) for x in EDGES] + [(x[1],x[3],x[5],x[7]) for x in EDGES]

    return render_to_response('network.txt', locals(), context_instance=RequestContext(request))


def search(request):
    """ This search is used to find central nodes """
    query = request.GET['query'].split()

    if len(request.GET['query']) >= 3:
        # Build query
        cv_ret = Cvterm.objects.filter(Q(name__icontains=request.GET['query']) & Q(cv__name='disease_ontology') | Q(cv__name='human_phenotype'))[0:8].values_list('name',flat=True)
        feature_ret = Feature.objects.filter(name__contains=request.GET['query'])[0:8].values_list('name',flat=True)
        ret_terms = list(cv_ret) + list(feature_ret)


    return HttpResponse(json.dumps(ret_terms),content_type="text/plain")
    