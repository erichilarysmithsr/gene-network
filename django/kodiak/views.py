from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from chado.models import *
from django.db import connection
from django.utils.datastructures import SortedDict
from django.db.models import Q
import simplejson as json
import operator
connection._rollback()




def home(request):

    TITLE = "Home"

    return render_to_response('home.txt', locals(), context_instance=RequestContext(request))



    



