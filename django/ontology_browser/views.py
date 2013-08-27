# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q
import simplejson as json
from chado.models import *


def browser(request, cv=None, branches = None):
    """ This is the view for the ontology browser """

    TITLE = "Ontology Browser"

    # Fetch Terms
    roots = CvRoot.objects.all().select_related().order_by('cv_id')
    terminals = CvLeaf.objects.filter(cvterm_id__in = roots.values('root_cvterm_id')).values_list('cvterm_id', flat=True)

    return render_to_response('browser.txt', locals(), context_instance=RequestContext(request))

def tree_req(request, cvterm_id):
    """ 
    Returns a JSON string for the ontology browser. Returned string is two parts:
    1) The clicked term information (title, definition, etc.)
    2) A list of child terms (if the term is not a leaf [terminal]).
    """
    cvt = Cvterm.objects.get(cvterm_id=cvterm_id)
    cv_terms = CvtermRelationship.objects.filter(Q(object__cvterm_id = cvterm_id))
    terminals = CvLeaf.objects.filter(cvterm_id__in = cv_terms.values('subject_id')).values_list('cvterm_id', flat=True)

    # Setup json response object and term info
    json_ret = {}
    json_ret['term'] = {}
    json_ret['term']['title'] = cvt.name
    json_ret['term']['definition'] = cvt.definition
    json_ret['term']['db'] = cvt.dbxref.db.name
    json_ret['term']['accession'] = cvt.dbxref.accession
    json_ret['term']['urlprefix'] = cvt.dbxref.db.urlprefix
    json_ret['term']['xrefs'] = list(cvt.xrefs.all().values('dbxref__db__name','dbxref__accession'))

    
    # Add data of child cv's if not a terminal node.
    json_ret['children'] = []
    for term in cv_terms:
        child = {}
        child['title'] = term.subject.name
        child['cvterm'] = term.subject.cvterm_id
        if term.subject.cvterm_id in terminals:
            child['terminal'] = True
        else:
            child['terminal'] = False

        json_ret['children'].append(child)
         
    # Return

    return HttpResponse(json.dumps(json_ret), content_type="text/plain")
