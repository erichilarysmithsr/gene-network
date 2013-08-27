# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

#### LIST of Currently working VIEWs ####
"""
CvRoot
CvLeaf
Dfeatureloc
"""

##########################################
#------ General Module - Identifiers-----#
##########################################

# Db - Database Authorities
# Describes the groups responsible for creating an identifier.
class Db(models.Model):
    db_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    urlprefix = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'db'

# Dbxref - 
# List of identifiers. General format: <DB>:<ACCESSION>:<VERSION>
class Dbxref(models.Model):
    dbxref_id = models.AutoField(primary_key=True)
    db = models.ForeignKey(Db)
    accession = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'dbxref'

    def __unicode__(self):
        return u'%s:%s' % (self.db, self.accession)

class Tableinfo(models.Model):
    tableinfo_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    primary_key_column = models.CharField(max_length=30, blank=True)
    is_view = models.IntegerField()
    view_on_table_id = models.IntegerField(null=True, blank=True)
    superclass_table_id = models.IntegerField(null=True, blank=True)
    is_updateable = models.IntegerField()
    modification_date = models.DateField()
    class Meta:
        db_table = 'tableinfo'

#----- General Module Views -----#

class DbDbxrefCount(models.Model):
    name = models.CharField(max_length=255, blank=True)
    num_dbxrefs = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'db_dbxref_count'

###############################################
#------ CV Module - Controlled Vocabulary-----#
###############################################

# Controlled Vocabulary
class Cv(models.Model):
    cv_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    definition = models.TextField(blank=True)

    class Meta:
        db_table = 'cv'

    def __unicode__(self):
        return self.name

class Cvterm(models.Model):
    cvterm_id = models.AutoField(primary_key=True)
    cv = models.ForeignKey("Cv", related_name="cv_set")
    name = models.CharField(max_length=1024)
    definition = models.TextField(blank=True)
    dbxref = models.ForeignKey('Dbxref', unique=True, related_name='dbxref_set')
    is_obsolete = models.IntegerField()
    is_relationshiptype = models.IntegerField()

    class Meta:
        db_table = 'cvterm'

    def __unicode__(self):
        return u'%s' % (self.name)

# Cvprop - Captures information regarding obo version of a loaded cv.
class Cvprop(models.Model):
    cvprop_id = models.IntegerField(primary_key=True)
    cv = models.ForeignKey(Cv)
    type = models.ForeignKey('Cvterm')
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'cvprop'

# This table contains additional/secondary identifiers (xrefs)
class CvtermDbxref(models.Model):
    cvterm_dbxref_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm, related_name='xrefs')
    dbxref = models.ForeignKey('Dbxref')
    is_for_definition = models.IntegerField()
    class Meta:
        db_table = 'cvterm_dbxref'

    def __unicode__(self):
        return u'%s, %s' % (self.cvterm, self.dbxref)

# Stores relationships between cvterms.
class CvtermRelationship(models.Model):
    cvterm_relationship_id = models.AutoField(primary_key=True, null=False)
    type = models.ForeignKey(Cvterm, related_name='cvterm_relationship_set', db_column="type_id")
    subject = models.ForeignKey(Cvterm, related_name = 'cvterm_relationship_subject')
    object = models.ForeignKey(Cvterm, related_name = 'cvterm_relationship_object')
    class Meta:
        db_table = 'cvterm_relationship'

    def __unicode__(self):
        return ("%s %s %s") % (self.subject, self.type, self.object)

# Stores the reflexive transitive closure of a relationship.
# e.g. 
class Cvtermpath(models.Model):
    cvtermpath_id = models.IntegerField(primary_key=True)
    type= models.ForeignKey(Cvterm, null=True, blank=True, related_name='cvtermpath_set')
    subject = models.ForeignKey(Cvterm, related_name='cvtermpath_subject_set')
    object = models.ForeignKey(Cvterm, related_name='cvtermpath_object_set')
    cv = models.ForeignKey(Cv)
    pathdistance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvtermpath'

class Cvtermprop(models.Model):
    cvtermprop_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey("Cvterm",  related_name="%(class)s_cvterm_set")
    type = models.ForeignKey("Cvterm", related_name="%(class)s_type_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'cvtermprop'


class Cvtermsynonym(models.Model):
    cvtermsynonym_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm, related_name="%(class)s_cvterm_set")
    synonym = models.CharField(max_length=1024)
    type = models.ForeignKey(Cvterm, null=True, blank=True, related_name="%(class)s_type_set")
    class Meta:
        db_table = 'cvtermsynonym'


class Dbxrefprop(models.Model):
    dbxrefprop_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'dbxrefprop'

#----- CV Module Views -----#

# the roots of a cv are the set of terms
# which have no parents (terms that are not the subject of a
# relation). Most CV's will have only a few roots.
class CvRoot(models.Model):
    cv_id = models.ForeignKey('Cv', db_column="cv_id", primary_key=True)
    root_cvterm_id = models.ForeignKey("Cvterm",db_column="root_cvterm_id")
    class Meta:
        unique_together = ('cv_id', 'root_cvterm_id')
        db_table = 'cv_root'
        managed = False

class CvLeaf(models.Model):
    cv_id = models.ForeignKey('Cv', db_column="cv_id", primary_key=True)
    cvterm_id = models.ForeignKey("Cvterm", db_column="cvterm_id")
    class Meta:
        unique_together = ('cv_id', 'cvterm_id')
        db_table = 'cv_leaf'
        managed = False


# CvCvtermCount - 
# per-cv terms counts (excludes obsoletes)
class CvCvtermCount(models.Model):
    name = models.CharField(max_length=255, blank=True)
    num_terms_excl_obs = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cv_cvterm_count'

# CvCvtermCountWithObs
# per-cv terms counts (includes obsoletes)
class CvCvtermCountWithObs(models.Model):
    name = models.CharField(max_length=255, blank=True)
    num_terms_incl_obs = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cv_cvterm_count_with_obs'

# CommonAncestorCvterm
# The common ancestor of any
# two terms is the intersection of both terms ancestors. Two terms can
# have multiple common ancestors. Use total_pathdistance to get the
# least common ancestor.
class CommonAncestorCvterm(models.Model):
    cvterm1_id = models.IntegerField(null=True, blank=True)
    cvterm2_id = models.IntegerField(null=True, blank=True)
    ancestor_cvterm_id = models.IntegerField(null=True, blank=True)
    pathdistance1 = models.IntegerField(null=True, blank=True)
    pathdistance2 = models.IntegerField(null=True, blank=True)
    total_pathdistance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'common_ancestor_cvterm'

# Common Descendent CvTerm
class CommonDescendantCvterm(models.Model):
    cvterm1_id = models.IntegerField(null=True, blank=True)
    cvterm2_id = models.IntegerField(null=True, blank=True)
    ancestor_cvterm_id = models.IntegerField(null=True, blank=True)
    pathdistance1 = models.IntegerField(null=True, blank=True)
    pathdistance2 = models.IntegerField(null=True, blank=True)
    total_pathdistance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'common_descendant_cvterm'

# 
class CvForFeature(models.Model):
    cv_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    definition = models.TextField(blank=True)
    class Meta:
        db_table = 'cv_for_feature'

class CvForFeatureRelationship(models.Model):
    cv_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    definition = models.TextField(blank=True)
    class Meta:
        db_table = 'cv_for_feature_relationship'

class CvForFeatureprop(models.Model):
    cv_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    definition = models.TextField(blank=True)
    class Meta:
        db_table = 'cv_for_featureprop'

class CvLinkCount(models.Model):
    cv_name = models.CharField(max_length=255, blank=True)
    relation_name = models.CharField(max_length=1024, blank=True)
    relation_cv_name = models.CharField(max_length=255, blank=True)
    num_links = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cv_link_count'

class CvPathCount(models.Model):
    cv_name = models.CharField(max_length=255, blank=True)
    relation_name = models.CharField(max_length=1024, blank=True)
    relation_cv_name = models.CharField(max_length=255, blank=True)
    num_paths = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cv_path_count'

class CvtermDifferentium(models.Model):
    cvterm_id = models.IntegerField(null=True, blank=True)
    cvterm_relationship_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvterm_differentium'

class CvtermGenus(models.Model):
    cvterm_id = models.IntegerField(null=True, blank=True)
    genus_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvterm_genus'

class CvtermLdefIntersection(models.Model):
    cvterm_relationship_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    typename = models.CharField(max_length=1024, blank=True)
    typeterm_cv_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvterm_ldef_intersection'


class CvtermRelationshipWithTypename(models.Model):
    cvterm_relationship_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    typename = models.CharField(max_length=1024, blank=True)
    typeterm_cv_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvterm_relationship_with_typename'

class CvtermpropWithPropname(models.Model):
    cvtermprop_id = models.IntegerField(null=True, blank=True)
    cvterm_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    value = models.TextField(blank=True)
    rank = models.IntegerField(null=True, blank=True)
    propname = models.CharField(max_length=1024, blank=True)
    propterm_cv_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvtermprop_with_propname'


class IsAnonymousCvterm(models.Model):
    cvterm_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'is_anonymous_cvterm'



#####################################
#------ Pub Module - Knowledge -----#
#####################################


class Pub(models.Model):
    pub_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True)
    volumetitle = models.TextField(blank=True)
    volume = models.CharField(max_length=255, blank=True)
    series_name = models.CharField(max_length=255, blank=True)
    issue = models.CharField(max_length=255, blank=True)
    pyear = models.CharField(max_length=255, blank=True)
    pages = models.CharField(max_length=255, blank=True)
    miniref = models.CharField(max_length=255, blank=True)
    uniquename = models.TextField(unique=True)
    type = models.ForeignKey('Cvterm')
    is_obsolete = models.NullBooleanField(null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pubplace = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'pub'

    def __unicode__(self):
        return "%s - %s:%s - %s" % (self.series_name, self.volume, self.issue, self.title)

class PubDbxref(models.Model):
    pub_dbxref_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = 'pub_dbxref'

class PubRelationship(models.Model):
    pub_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey("Pub", related_name="%(class)s_subject_set")
    object = models.ForeignKey("Pub", related_name="%(class)s_object_set")
    type = models.ForeignKey("Cvterm", related_name="%(class)s_type_set")
    class Meta:
        db_table = 'pub_relationship'

class Pubauthor(models.Model):
    pubauthor_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    rank = models.IntegerField()
    editor = models.NullBooleanField(null=True, blank=True)
    surname = models.CharField(max_length=100)
    givennames = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'pubauthor'

class Pubprop(models.Model):
    pubprop_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'pubprop'

#----- No Views -----#

################################################
#------ Sequence Module - DNA/RNA/Protein -----#
################################################

class Feature(models.Model):
    feature_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref, null=True, blank=True)
    organism = models.ForeignKey('Organism')
    name = models.CharField(max_length=255, blank=True)
    uniquename = models.TextField()
    residues = models.TextField(blank=True)
    seqlen = models.IntegerField(null=True, blank=True)
    md5checksum = models.CharField(max_length=32, blank=True)
    type = models.ForeignKey(Cvterm)
    is_analysis = models.BooleanField()
    is_obsolete = models.BooleanField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    
    class Meta:
        db_table = 'feature'

    def __unicode__(self):
        return u'%s' % (self.name)


class FeatureDbxref(models.Model):
    feature_dbxref_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, related_name='feature_xrefs')
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = 'feature_dbxref'

    def __unicode__(self):
        return u'%s' % (self.dbxref)

# Displays features and locations with coordinates relative to parent chromosome.
# For displaying feature locations relative to Parent Chromosome - use 'dfeatureloc'
class Featureloc(models.Model):
    featureloc_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey("Feature", related_name='feature_loc_set')
    srcfeature = models.ForeignKey("Feature", related_name='srcfeature_set',null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    is_fmin_partial = models.BooleanField()
    fmax = models.IntegerField(null=True, blank=True)
    is_fmax_partial = models.BooleanField()
    strand = models.SmallIntegerField(null=True, blank=True)
    phase = models.IntegerField(null=True, blank=True)
    residue_info = models.TextField(blank=True)
    locgroup = models.IntegerField()
    rank = models.IntegerField()
    
    class Meta:
        db_table = 'featureloc'

class FeatureCvterm(models.Model):
    feature_cvterm_id = models.AutoField(primary_key=True)
    feature = models.ForeignKey("Feature", related_name="fc_cvterm_set")
    cvterm = models.ForeignKey("Cvterm", related_name="fc_feature_set")
    pub = models.ForeignKey('Pub')
    is_not = models.BooleanField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_cvterm'

    def __unicode__(self):
        return unicode('%s - %s' % (self.feature,self.cvterm))

class FeatureCvtermDbxref(models.Model):
    feature_cvterm_dbxref_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = 'feature_cvterm_dbxref'

class FeatureCvtermPub(models.Model):
    feature_cvterm_pub_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'feature_cvterm_pub'

class FeatureCvtermprop(models.Model):
    feature_cvtermprop_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_cvtermprop'

class FeaturePub(models.Model):
    feature_pub_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'feature_pub'

class FeaturePubprop(models.Model):
    feature_pubprop_id = models.IntegerField(primary_key=True)
    feature_pub = models.ForeignKey(FeaturePub)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_pubprop'

class FeatureRelationship(models.Model):
    feature_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Feature, related_name='featurerelationship_subject_set')
    object = models.ForeignKey(Feature, related_name='featurerelationship_object_set')
    type = models.ForeignKey(Cvterm, related_name='featurerelationship_object_set')
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_relationship'

    def __unicode__(self):
        return unicode("%s %s %s" % (self.subject, self.type, self.object))

class FeatureRelationshipPub(models.Model):
    feature_relationship_pub_id = models.IntegerField(primary_key=True)
    feature_relationship = models.ForeignKey(FeatureRelationship)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'feature_relationship_pub'

class FeatureRelationshipprop(models.Model):
    feature_relationshipprop_id = models.IntegerField(primary_key=True)
    feature_relationship = models.ForeignKey(FeatureRelationship)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_relationshipprop'

class FeatureRelationshippropPub(models.Model):
    feature_relationshipprop_pub_id = models.IntegerField(primary_key=True)
    feature_relationshipprop = models.ForeignKey(FeatureRelationshipprop)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'feature_relationshipprop_pub'

class FeatureSynonym(models.Model):
    feature_synonym_id = models.AutoField(primary_key=True)
    synonym = models.ForeignKey('Synonym')
    feature = models.ForeignKey(Feature,related_name='synonym')
    pub = models.ForeignKey('Pub', null=True)
    is_current = models.BooleanField()
    is_internal = models.BooleanField()
    class Meta:
        db_table = 'feature_synonym'

    def __unicode__(self):
        return unicode("%s (%s) %s" % (self.feature,self.synonym.name,self.pub))


class FeaturelocPub(models.Model):
    featureloc_pub_id = models.IntegerField(primary_key=True)
    featureloc = models.ForeignKey(Featureloc)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'featureloc_pub'

class Featureprop(models.Model):
    featureprop_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, related_name="feature_prop_set")
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        db_table = 'featureprop'

class FeaturepropPub(models.Model):
    featureprop_pub_id = models.IntegerField(primary_key=True)
    featureprop = models.ForeignKey(Featureprop)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'featureprop_pub'

class Synonym(models.Model):
    synonym_id = models.AutoField(primary_key=True, db_column="synonym_id")
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Cvterm, db_column="type_id")
    synonym_sgml = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'synonym'
        unique_together = ('name','type',)


    def __unicode__(self):
        return unicode('%s %s %s' % (self.name,self.type,self.synonym_sgml))

#----- Sequence Views -----#

# Relative!
class Dfeatureloc(models.Model):
    featureloc_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey("Feature", db_column='feature_id', related_name='dfeature_loc_set')
    srcfeature = models.ForeignKey("Feature", db_column='feature_id',null=True, blank=True)
    nbeg = models.IntegerField(null=True, blank=True)
    is_nbeg_partial = models.NullBooleanField(null=True, blank=True)
    nend = models.IntegerField(null=True, blank=True)
    is_nend_partial = models.NullBooleanField(null=True, blank=True)
    strand = models.SmallIntegerField(null=True, blank=True)
    phase = models.IntegerField(null=True, blank=True)
    residue_info = models.TextField(blank=True)
    locgroup = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'dfeatureloc'
        managed = False


class FeatureContains(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_contains'


class FeatureDifference(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    srcfeature_id = models.SmallIntegerField(null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    fmax = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_difference'

class FeatureDisjoint(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_disjoint'


class FeatureDistance(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    srcfeature_id = models.IntegerField(null=True, blank=True)
    subject_strand = models.SmallIntegerField(null=True, blank=True)
    object_strand = models.SmallIntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_distance'

class FeatureIntersection(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    srcfeature_id = models.IntegerField(null=True, blank=True)
    subject_strand = models.SmallIntegerField(null=True, blank=True)
    object_strand = models.SmallIntegerField(null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    fmax = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_intersection'

class FeatureMeets(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_meets'

class FeatureMeetsOnSameStrand(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_meets_on_same_strand'


class FeatureUnion(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    srcfeature_id = models.IntegerField(null=True, blank=True)
    subject_strand = models.SmallIntegerField(null=True, blank=True)
    object_strand = models.SmallIntegerField(null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    fmax = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_union'


class FeaturesetMeets(models.Model):
    subject_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'featureset_meets'


class IntronCombinedView(models.Model):
    exon1_id = models.IntegerField(null=True, blank=True)
    exon2_id = models.IntegerField(null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    fmax = models.IntegerField(null=True, blank=True)
    strand = models.SmallIntegerField(null=True, blank=True)
    srcfeature_id = models.IntegerField(null=True, blank=True)
    intron_rank = models.IntegerField(null=True, blank=True)
    transcript_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'intron_combined_view'

class IntronlocView(models.Model):
    exon1_id = models.IntegerField(null=True, blank=True)
    exon2_id = models.IntegerField(null=True, blank=True)
    fmin = models.IntegerField(null=True, blank=True)
    fmax = models.IntegerField(null=True, blank=True)
    strand = models.SmallIntegerField(null=True, blank=True)
    srcfeature_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'intronloc_view'


class TypeFeatureCount(models.Model):
    type = models.CharField(max_length=1024, blank=True)
    num_features = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'type_feature_count'

class StatsPathsToRoot(models.Model):
    cvterm_id = models.IntegerField(null=True, blank=True)
    total_paths = models.BigIntegerField(null=True, blank=True)
    avg_distance = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    min_distance = models.IntegerField(null=True, blank=True)
    max_distance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'stats_paths_to_root'

##############################
#------ Organism Module -----#
##############################


class Organism(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = 'organism'

    def __unicode__(self):
        return unicode(self.common_name)

class OrganismDbxref(models.Model):
    organism_dbxref_id = models.IntegerField(primary_key=True)
    organism = models.ForeignKey(Organism)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = 'organism_dbxref'

class Organismprop(models.Model):
    organismprop_id = models.IntegerField(primary_key=True)
    organism = models.ForeignKey(Organism)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'organismprop'

#----- No Views -----#

##############################
#------  Module -----#
##############################

class Chadoprop(models.Model):
    chadoprop_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey('Cvterm')
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'chadoprop'



class MaterializedView(models.Model):
    materialized_view_id = models.IntegerField()
    last_update = models.DateTimeField(null=True, blank=True)
    refresh_time = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=64, unique=True, blank=True)
    mv_schema = models.CharField(max_length=64, blank=True)
    mv_table = models.CharField(max_length=128, blank=True)
    mv_specs = models.TextField(blank=True)
    indexed = models.TextField(blank=True)
    query = models.TextField(blank=True)
    special_index = models.TextField(blank=True)
    class Meta:
        db_table = 'materialized_view'





