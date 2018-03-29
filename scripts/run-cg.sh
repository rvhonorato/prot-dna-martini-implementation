#!/bin/bash

#----------------------------------------------------------------------------------------------------------------#
# INPUT
#----------------------------------------------------------------------------------------------------------------#

CGTOAA_RESTRAIN=aa2cg.tbl
AMBIG_RESTRAIN=ambig.tbl

PDBA_AA=$1
PDBB_AA=$2

#----------------------------------------------------------------------------------------------------------------#
#
# SET UP CG RUN 
#
#----------------------------------------------------------------------------------------------------------------#

PDBA_CG=${PDBA_AA%.*}_cg.pdb
PDBB_CG=${PDBB_AA%.*}_cg.pdb

printf "
<html>
<head>
<title>HADDOCK - start</title>
</head>
<body bgcolor=#ffffff>
<h2>Parameters for the start:</h2>
<BR>
<h4><!-- HADDOCK -->
CGTOAA_TBL=./%s<BR>
AMBIG_TBL=./%s<BR>
HADDOCK_DIR=/home/abonvin/haddock2.3/<BR>
N_COMP=2<BR>
PDB_FILE1=./%s<BR>
CGPDB_FILE1=./%s<BR>
PDB_FILE2=./%s<BR>
CGPDB_FILE2=./%s<BR>
PROJECT_DIR=./<BR>
PROT_SEGID_1=A<BR>
PROT_SEGID_2=B<BR>
RUN_NUMBER=1<BR>
submit_save=Save updated parameters<BR>
</h4><!-- HADDOCK -->
</body>
</html>" "$CGTOAA_RESTRAIN" "$AMBIG_RESTRAIN" "$PDBA_AA" "$PDBA_CG" "$PDBB_AA" "$PDBB_CG" > new.html

/usr/bin/python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py

cd run1

#----------------------------------------------------------------------------------------------------------------#
#
# Copy new files
#
#----------------------------------------------------------------------------------------------------------------#
PARAM_FOLDER=/home/rodrigo/cg-params

# Add CG topology, parameters, link and patches
cp $PARAM_FOLDER/dna-cg.top toppar/
cp $PARAM_FOLDER/dna-cg.param toppar/
cp $PARAM_FOLDER/dna-cg.link toppar/
cp $PARAM_FOLDER/dna-cg-break.top toppar/

cp $PARAM_FOLDER/patch-types-cg-hbond-dna.cns protocols/
cp $PARAM_FOLDER/dna-cg-break.cns protocols/

#----------------------------------------------------------------------------------------------------------------#
#
# Edit run.cns 
#
#----------------------------------------------------------------------------------------------------------------#

sed -i 's/{===>} cg_A=false;/{===>} cg_A=true;/g' run.cns
sed -i 's/{===>} cg_B=false;/{===>} cg_B=true;/g' run.cns
sed -i 's/{===>} dna_B=false;/{===>} dna_B=true;/g' run.cns
sed -i 's/{===>} prot_top_B="protein-allhdg5-4.top";/{===>} prot_top_B="dna-rna-allatom-hj-opls-1.3.top";/g' run.cns
sed -i 's/{===>} prot_link_B="protein-allhdg5-4-noter.link";/{===>} prot_link_B="dna-rna-1.3.link";/g' run.cns
sed -i 's/{===>} prot_par_B="protein-allhdg5-4.param";/{===>} prot_par_B="dna-rna-allatom-hj-opls-1.3.param";/g' run.cns
sed -i 's/{===>} prot_cg_top_B="protein-CG-Martini-2-2.top";/{===>} prot_cg_top_B="dna-cg.top";/g' run.cns
sed -i 's/{===>} prot_cg_link_B="protein-CG-Martini-2-2.link";/{===>} prot_cg_link_B="dna-cg.link";/g' run.cns
sed -i 's/{===>} prot_cg_par_B="protein-CG-Martini-2-2.param";/{===>} prot_cg_par_B="dna-cg.param";/g' run.cns

sed -i '/{===>} dnarest_on=false;/a {===>} dnacgrest_on=true;' run.cns
sed -i '/evaluate (&Data.dnarest = &dnarest_on)/a evaluate (&Data.dnacgrest = &dnacgrest_on)' run.cns

# water phase configs
sed -i 's/{===>} solvshell=true;/{===>} solvshell=false;/g' run.cns

#----------------------------------------------------------------------------------------------------------------#
#
# Edit input generator
#
#----------------------------------------------------------------------------------------------------------------#

# cp protocols/generate_B-cg.inp protocols/generate_B-cg.inp-bak

sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna.cns' protocols/generate_B-cg.inp
sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/dna-cg-break.cns' protocols/generate_B-cg.inp
sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_B-cg.inp
sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/dna-cg-break.top";' protocols/generate_B-cg.inp
sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_B-cg.inp

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/dna-cg.top/g' protocols/generate_B-cg.inp
sed -i 's/dna-rna-1.3.link/dna-cg.link/g' protocols/generate_B-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/dna-cg.param/g' protocols/generate_B-cg.inp

#----------------------------------------------------------------------------------------------------------------#
#
# Edit refine input
#
#----------------------------------------------------------------------------------------------------------------#

sed -i '/if ($Data.dnarest eq true ) then/i if ($DATA.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-cg_restraints.def\nend if\n' protocols/refine.inp

# TEMPORARY !!!

cp $PARAM_FOLDER/dna-cg_restraints.def data/sequence/


#----------------------------------------------------------------------------------------------------------------#

# cd ..

# #----------------------------------------------------------------------------------------------------------------#
# #
# # SET UP AA RUN 
# #
# #----------------------------------------------------------------------------------------------------------------#

# printf "
# <html>
# <head>
# <title>HADDOCK - start</title>
# </head>
# <body bgcolor=#ffffff>
# <h2>Parameters for the start:</h2>
# <BR>
# <h4><!-- HADDOCK -->
# AMBIG_TBL=./%s<BR>
# HADDOCK_DIR=/home/abonvin/haddock2.3/<BR>
# N_COMP=2<BR>
# PDB_FILE1=./%s<BR>
# PDB_FILE2=./%s<BR>
# PROJECT_DIR=./<BR>
# PROT_SEGID_1=A<BR>
# PROT_SEGID_2=B<BR>
# RUN_NUMBER=2<BR>
# submit_save=Save updated parameters<BR>
# </h4><!-- HADDOCK -->
# </body>
# </html>" "$AMBIG_RESTRAIN" "$PDBA_AA" "$PDBB_AA" > new.html

# /usr/bin/python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py

# cd run2

# #----------------------------------------------------------------------------------------------------------------#
# #
# # Edit run.cns 
# #
# #----------------------------------------------------------------------------------------------------------------#
# sed -i 's/{===>} dna_B=false;/{===>} dna_B=true;/g' run.cns
# sed -i 's/{===>} prot_top_B="protein-allhdg5-4.top";/{===>} prot_top_B="dna-rna-allatom-hj-opls-1.3.top";/g' run.cns
# sed -i 's/{===>} prot_link_B="protein-allhdg5-4-noter.link";/{===>} prot_link_B="dna-rna-1.3.link";/g' run.cns
# sed -i 's/{===>} prot_par_B="protein-allhdg5-4.param";/{===>} prot_par_B="dna-rna-allatom-hj-opls-1.3.param";/g' run.cns

# #----------------------------------------------------------------------------------------------------------------#
# # execute?


