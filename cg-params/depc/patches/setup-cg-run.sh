#!/bin/bash

DNA_CHAIN=C

cd run1

#----------------------------------------------------------------------------------------------------------------#
# Copy new files
#----------------------------------------------------------------------------------------------------------------#
PARAM_FOLDER=/home/rodrigo/cg-params/toppar
CG_TOP=$PARAM_FOLDER/dna-CG-MARTINI-2-1p.top
CG_PARAM=$PARAM_FOLDER/dna-CG-MARTINI-2-1p.param
CG_LINK=$PARAM_FOLDER/dna-CG-MARTINI-2-1p.link
CG_DNA_BREAK_TOP=$PARAM_FOLDER/dna-CG-MARTINI-2-1p-break.top

PATCHES_FOLDER=/home/rodrigo/cg-params/patches
CG_HBONDS=$PATCHES_FOLDER/patch-types-cg-hbond-dna.cns
CG_DNA_BREAKS=$PATCHES_FOLDER/dna-cg-break.cns

# Add CG topology, parameters, link and patches
cp $CG_TOP toppar/
cp $CG_PARAM toppar/
cp $CG_LINK toppar/
cp $CG_DNA_BREAK_TOP toppar/

cp $CG_HBONDS protocols/
cp $CG_DNA_BREAKS protocols/

#----------------------------------------------------------------------------------------------------------------#
# Edit run.cns 
#----------------------------------------------------------------------------------------------------------------#

# set AA DNA toppar 
sed -i "s/{===>} dna_$DNA_CHAIN=false;/{===>} dna_$DNA_CHAIN=true;/g" run.cns

sed -i "s/{===>} prot_top_$DNA_CHAIN=\"protein-allhdg5-4.top\";/{===>} prot_top_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.top\";/g" run.cns
sed -i "s/{===>} prot_link_$DNA_CHAIN=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_$DNA_CHAIN=\"dna-rna-1.3.link\";/g" run.cns
sed -i "s/{===>} prot_par_$DNA_CHAIN=\"protein-allhdg5-4.param\";/{===>} prot_par_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.param\";/g" run.cns

# set CG DNA toppar
sed -i "s/{===>} prot_cg_top_$DNA_CHAIN=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_$DNA_CHAIN=\"dna-cg.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_$DNA_CHAIN=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_$DNA_CHAIN=\"dna-cg.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_$DNA_CHAIN=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_$DNA_CHAIN=\"dna-cg.param\";/g" run.cns

# add DNA CG restrictions
sed -i '/{===>} dnarest_on=false;/a {===>} dnacgrest_on=true;' run.cns
sed -i 's/{===>} dnarest_on=false;/{===>} dnarest_on=true;/g' run.cns

sed -i '/evaluate (&Data.dnarest = &dnarest_on)/a evaluate (&Data.dnacgrest = &dnacgrest_on)' run.cns

# change options
sed -i 's/{===>} solvshell=true;/{===>} solvshell=false;/g' run.cns

#----------------------------------------------------------------------------------------------------------------#
# Edit input generator
#----------------------------------------------------------------------------------------------------------------#

# add patch to correct bead types for special hydrogen bonding
sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna.cns' protocols/generate_$DNA_CHAIN-cg.inp
# add dna-cg break files
sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/dna-cg-break.cns' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/dna-cg-break.top";' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_$DNA_CHAIN-cg.inp

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/dna-cg.top/g' protocols/generate_$DNA_CHAIN-cg.inp
sed -i 's/dna-rna-1.3.link/dna-cg.link/g' protocols/generate_$DNA_CHAIN-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/dna-cg.param/g' protocols/generate_$DNA_CHAIN-cg.inp

#----------------------------------------------------------------------------------------------------------------#
# Edit refine input
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
