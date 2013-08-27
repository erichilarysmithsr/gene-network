# Create your views here.
from chado.models import *

import django_databrowse

django_databrowse.site.register(Cv, Db, Cvterm, Dbxref, Feature, FeatureSynonym, CvtermRelationship, FeatureRelationship, FeatureCvterm)
