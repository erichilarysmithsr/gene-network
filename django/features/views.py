# Create your views here.
from django.shortcuts import render_to_response
from chado.models import *


def search_features(request):

	if 'q' in request.GET:
		query = request.GET['q']
		results = Feature.objects.select_related().filter(name__icontains=query)

	return render_to_response('features.txt', locals())