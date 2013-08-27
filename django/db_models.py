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

class Chadoprop(models.Model):
    chadoprop_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey('Cvterm')
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'chadoprop'

class Cv(models.Model):
    cv_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    definition = models.TextField(blank=True)
    class Meta:
        db_table = 'cv'

class Cvprop(models.Model):
    cvprop_id = models.IntegerField(primary_key=True)
    cv = models.ForeignKey(Cv)
    type = models.ForeignKey('Cvterm')
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'cvprop'

class Cvterm(models.Model):
    cvterm_id = models.IntegerField(primary_key=True)
    cv = models.ForeignKey(Cv)
    name = models.CharField(max_length=1024)
    definition = models.TextField(blank=True)
    dbxref = models.ForeignKey('Dbxref', unique=True)
    is_obsolete = models.IntegerField()
    is_relationshiptype = models.IntegerField()
    class Meta:
        db_table = 'cvterm'

class CvtermDbxref(models.Model):
    cvterm_dbxref_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm)
    dbxref = models.ForeignKey('Dbxref')
    is_for_definition = models.IntegerField()
    class Meta:
        db_table = 'cvterm_dbxref'

class CvtermRelationship(models.Model):
    cvterm_relationship_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    subject = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Cvterm)
    class Meta:
        db_table = 'cvterm_relationship'

class Cvtermpath(models.Model):
    cvtermpath_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm, null=True, blank=True)
    subject = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Cvterm)
    cv = models.ForeignKey(Cv)
    pathdistance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cvtermpath'

class Cvtermprop(models.Model):
    cvtermprop_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'cvtermprop'

class Cvtermsynonym(models.Model):
    cvtermsynonym_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm)
    synonym = models.CharField(max_length=1024)
    type = models.ForeignKey(Cvterm, null=True, blank=True)
    class Meta:
        db_table = 'cvtermsynonym'

class Db(models.Model):
    db_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    urlprefix = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'db'

class Dbxref(models.Model):
    dbxref_id = models.IntegerField(primary_key=True)
    db = models.ForeignKey(Db)
    accession = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'dbxref'

class Dbxrefprop(models.Model):
    dbxrefprop_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'dbxrefprop'

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

class FeatureCvterm(models.Model):
    feature_cvterm_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey('Pub')
    is_not = models.BooleanField()
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_cvterm'

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

class FeatureDbxref(models.Model):
    feature_dbxref_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = 'feature_dbxref'

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
    subject = models.ForeignKey(Feature)
    object = models.ForeignKey(Feature)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'feature_relationship'

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
    feature_synonym_id = models.IntegerField(primary_key=True)
    synonym = models.ForeignKey('Synonym')
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey('Pub')
    is_current = models.BooleanField()
    is_internal = models.BooleanField()
    class Meta:
        db_table = 'feature_synonym'

class Featureloc(models.Model):
    featureloc_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    srcfeature = models.ForeignKey(Feature, null=True, blank=True)
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

class FeaturelocPub(models.Model):
    featureloc_pub_id = models.IntegerField(primary_key=True)
    featureloc = models.ForeignKey(Featureloc)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'featureloc_pub'

class Featureprop(models.Model):
    featureprop_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    type = models.ForeignKey(Cvterm)
    value = models.TextField(blank=True)
    rank = models.IntegerField()
    class Meta:
        db_table = 'featureprop'

class FeaturepropPub(models.Model):
    featureprop_pub_id = models.IntegerField(primary_key=True)
    featureprop = models.ForeignKey(Featureprop)
    pub = models.ForeignKey('Pub')
    class Meta:
        db_table = 'featureprop_pub'

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

class Organism(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = 'organism'

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

class Pub(models.Model):
    pub_id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True)
    volumetitle = models.TextField(blank=True)
    volume = models.CharField(max_length=255, blank=True)
    series_name = models.CharField(max_length=255, blank=True)
    issue = models.CharField(max_length=255, blank=True)
    pyear = models.CharField(max_length=255, blank=True)
    pages = models.CharField(max_length=255, blank=True)
    miniref = models.CharField(max_length=255, blank=True)
    uniquename = models.TextField(unique=True)
    type = models.ForeignKey(Cvterm)
    is_obsolete = models.BooleanField(null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pubplace = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'pub'

class PubDbxref(models.Model):
    pub_dbxref_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = 'pub_dbxref'

class PubRelationship(models.Model):
    pub_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Pub)
    object = models.ForeignKey(Pub)
    type = models.ForeignKey(Cvterm)
    class Meta:
        db_table = 'pub_relationship'

class Pubauthor(models.Model):
    pubauthor_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    rank = models.IntegerField()
    editor = models.BooleanField(null=True, blank=True)
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

class Synonym(models.Model):
    synonym_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Cvterm)
    synonym_sgml = models.CharField(max_length=255)
    class Meta:
        db_table = 'synonym'

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

