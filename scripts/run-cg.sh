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
echo "> Setting CG run"
echo ""
echo "> Writing new.html"
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

sed -i 's/{===>} dnarest_on=false;/{===>} dnarest_on=true;/g' run.cns

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

#======================================================#
#  THIS IS NOT A PERMANENT (OR EVEN A GOOD) SOLUTION!  #
#======================================================#
# Remove these lines (1360-1362)
#
##if ($Data.dnarest eq true ) then
##  @RUN:data/sequence/dna-rna_restraints.def
##end if
#
sed -i '1360,1362d' protocols/refine.inp

# Add these
#
##if ($DATA.dnacgrest eq true ) then
##  @RUN:data/sequence/dna-cg_restraints.def
##else
##  if ($Data.dnarest eq true ) then
##    @RUN:data/sequence/dna-rna_restraints.def
##  end if
##end if
#
sed -i "1360i if (\$Data.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-cg_restraints.def\nelse\n\ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ end if\nend if" protocols/refine.inp 

# Same, but for other part of the code
sed -i '1784,1786d' protocols/refine.inp
# identation is different
sed -i "1784i \ \ if (\$Data.dnacgrest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-cg_restraints.def\n\ \ else\n\ \ \ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ \ \ end if\n\ \ end if" protocols/refine.inp 

#----------------------------------------------------------------------------------------------------------------#
#
# Write DNA-AA restraints
#
#----------------------------------------------------------------------------------------------------------------#

#====#
#
# The files dna-aa_groups.dat and cg_restraints.def are generated by the aa2cg-prot_dna.py script!
#
# dna-rna_restraints-ori.def and dna-cg_restraints-ori.def are edited versions of the files generated by default
#  by HADDOCK, these two files are ready for the following edits. It will not work with any other file!
#
#====#

# add restraints to line 308 of dna-rna_restraints-ori.def
sed "308r ../cg_restraints.def" $PARAM_FOLDER/dna-rna_restraints-ori.def > data/sequence/dna-rna_restraints.def

# get groups
AAGROUP_1=$(sed -n '1p' ../dna-aa_groups.dat)
SEGID_1=$(sed -n '2p' ../dna-aa_groups.dat) 
AAGROUP_2=$(sed -n '3p' ../dna-aa_groups.dat)
SEGID_2=$(sed -n '4p' ../dna-aa_groups.dat) 

sed -i "s/{===>} bases_planar=((resid 1:20 or resid 21:40) and segid B);/{===>} bases_planar=((resid $AAGROUP_1 or resid $AAGROUP_2) and segid B);/g" data/sequence/dna-rna_restraints.def

sed -i "s/{===>} pucker_1=(resid 1:20 and segid B);/{===>} pucker_1=(resid $AAGROUP_1 and segid $SEGID_1);/g" data/sequence/dna-rna_restraints.def
sed -i "s/{===>} pucker_2=(resid 21:40 and segid B);/{===>} pucker_2=(resid $AAGROUP_2 and segid $SEGID_2);/g" data/sequence/dna-rna_restraints.def

sed -i "s/{===>} dihedral_1=(resid 1:20 and segid B);/{===>} dihedral_1=(resid $AAGROUP_1 and segid $SEGID_1);/g" data/sequence/dna-rna_restraints.def
sed -i "s/{===>} dihedral_2=(resid 21:40 and segid B);/{===>} dihedral_2=(resid $AAGROUP_2 and segid $SEGID_2);/g" data/sequence/dna-rna_restraints.def

sed -i 's/{===>} basepair_planar=false;/{===>} basepair_planar=true;/g' data/sequence/dna-rna_restraints.def

#----------------------------------------------------------------------------------------------------------------#
#
# Write DNA-CG restraints
#
#----------------------------------------------------------------------------------------------------------------#

# add restraints to line 18 of dna-rna_restraints-ori.def
sed "18r ../cg_restraints.def" $PARAM_FOLDER/dna-cg_restraints-ori.def > data/sequence/dna-cg_restraints.def


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


