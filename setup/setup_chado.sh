#!/usr/bin/env

# Requires wget - can be installed using homebrew if you are on a mac.

## Installation Variables ##
CHADO_DB_USERNAME=""
CHADO_DB_PASS="" 
CHADO_DB_NAME="chado"
PATH_TO_PSQL="/Applications/Postgres.app/Contents/MacOS/bin/psql" # I use a special application for mac, for convenience.

$PATH_TO_PSQL <<EOF
CREATE database $CHADO_DB_NAME;
EOF

#############################
# Download the Chado Schema #
#############################

# Download chado schema
wget --timestamping http://sourceforge.net/projects/gmod/files/gmod/chado-1.23/chado-1.23.tar.gz/download -O chado-1.23.tar.gz

# Unzip
gunzip chado-1.23.tar.gz
tar -xf chado-1.23.tar

# Remove unnecessary files.
rm chado-1.23.tar

cd chado-1.23

##########################################
# Install Perl Dependencies if necessary #
##########################################

# Install Perl Dependencies
# Some of these are used later on.
sudo perl -MCPAN -e shell <<EOF
install GO::Parser
install Template
install version
install SQL::Translator
force install DBD::Pg
install Bio::Chado::Schema
install DBIx::DBSchema
install XML::Parser::PerlSAX
force install DBIx::DBStag
install Config::Std
install Getopt::Long
EOF

########
# MAKE #
########

perl Makefile.PL  CHADO_DB_NAME=$CHADO_DB_NAME CHADO_DB_USERNAME=$CHADO_DB_USERNAME  CHADO_DB_PASS=$CHADO_DB_PASS GO_ROOT=$HOME

# For Reference:
#      -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*WARNING-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#               STEP 3 WILL DELETE ANY DATA IN A DATABASE WITH THE 
#                  DATABASE NAME YOU PROVIDED!
#      -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*WARNING-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#        3a. make load_schema (loads SQL schema into database)
#      
#      or
#      
#        3b. make update     (update an old Chado schema and stop here)
#        4. make prepdb      (loads basic data)
#        5. make ontologies  (loads data for various ontologies)
#      
#      Optional Targets:
#        make rm_locks     (removes ontology lock files, allowing installation
#                           of ontologies on successive builds of the database
#                           without removing the ontology files altogether)
#        make clean        (remove build related files and ontology tmp dir)
#        make instructions (at any moment display these instructions)
#      
#      -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


#################
# Install Chado #
#################
 perl Makefile.PL
 make
 sudo make install
 make load_schema
 make prepdb
 make ontologies  #selected 1,2,3,4
# Install, load scheme, prep db, and load ontologies.
sudo make install # Sets up install files.
make load_schema # Load a blank Schema
make prepdb # Prepare the database; Inserts a few funamentals.
make ontologies # Install ontologies. 
1,2,3,4 # Relationship, Sequence, Gene, and feature

cd ..

##################################
# Download additional ontologies #
##################################
mkdir obo
# Human Phenotype
wget --timestamping --directory-prefix=obo "http://compbio.charite.de/hudson/job/hpo/lastSuccessfulBuild/artifact/ontology/release/hp.obo"

# Disease Ontology
wget --timestamping --directory-prefix=obo "http://purl.obolibrary.org/obo/doid.obo"

# Create a directory for storing the xml files.
mkdir obo_xml

# Create XML Files of each ontology.
go2fmt.pl -p obo_text -w xml obo/hp.obo | \
            go-apply-xslt oboxml_to_chadoxml - > obo_xml/hp_obo.xml

# Within the disease ontology; some URLS need to be truncated b/c they were violating the chado schema.
python <<EOF
import re
f = file("obo/doid.obo",'r').read()
fixed = file("obo/doid_fixed.obo",'w')
def match_repl(m):
  return m.group(0)[0:239] # Truncate long urls

m = re.subn( r'url:(.*)[,|\]]',match_repl,f)

fixed.write(m[0])
EOF

##################################
# Load Additional Ontologies     #
##################################

# Use the fixed disease ontolgoy file to create the xml file.
go2fmt.pl -p obo_text -w xml obo/doid_fixed.obo | \
            go-apply-xslt oboxml_to_chadoxml - > obo_xml/doid_obo.xml


# Finally - load the remaining obo's
stag-storenode.pl \
     -d 'dbi:Pg:dbname=chado;host=localhost;port=5432' \
     --user $CHADO_DB_USERNAME obo_xml/hp_obo.xml


stag-storenode.pl \
     -d 'dbi:Pg:dbname=chado;host=localhost;port=5432' \
     --user $CHADO_DB_USERNAME obo_xml/doid_obo.xml




####################################
# Download Human Features and Load #
####################################
cd add_db # Directory used to store files of databases being added.
mkdir gff3
cd gff3
wget 'https://biotoolbox.googlecode.com/svn-history/r600/trunk/scripts/ucsc_table2gff3.pl'
perl ucsc_table2gff3.pl --ftp refgene --db hg19 --table refGene --nocds

# Load Chromosomes
gmod_gff3_preprocessor.pl --gfffile 'hg19_chromInfo.gff3'
gmod_bulk_load_gff3.pl --gfffile 'hg19_chromInfo.gff3.sorted' --recreate_cache

# Load Data
# gmod_gff3_preprocessor.pl --gfffile 'hg19_refGene.gff3' # Apparently, you do not need to pre-process this file.
gmod_bulk_load_gff3.pl --gfffile 'hg19_refGene.gff3' --dbxref 


