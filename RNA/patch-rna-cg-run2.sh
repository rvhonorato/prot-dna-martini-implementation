#!/bin/bash
#
#================================================================================================================#
# RNA
#================================================================================================================#
#
# run1: act-pass epsilon=78
# run2: act-pass-nodesol epsilon=78, w_desol = 0.0
# run3: CM
# run4: CM-nodesol
#
#================================================================================================================#

#----------------------------------------------------------------------------------------------------------------#
# SET UP CG RUN 
#----------------------------------------------------------------------------------------------------------------#
echo "> Setting CG run"

cd run2

#----------------------------------------------------------------------------------------------------------------#
# Run specific parameters
#----------------------------------------------------------------------------------------------------------------#

sed -i 's/{===>} epsilon=10.0;/{===>} epsilon=78.0;/g' run.cns

sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

##################################################################################################################
# From here on its the same...
##################################################################################################################

#----------------------------------------------------------------------------------------------------------------#
# INPUT
#----------------------------------------------------------------------------------------------------------------#

DNA_CHAIN=$1

# Add CG topology, parameters, link and patches
PARAM_FOLDER=/home/rodrigo/cg-params/

CG_TOP=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.top
CG_PARAM=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.param
CG_LINK=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.link
CG_DNA_BREAK_TOP=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p-break.top

CG_HBONDS=$PARAM_FOLDER/patch-types-cg-hbond-dna-rna.cns
CG_DNA_BREAKS=$PARAM_FOLDER/patch-breaks-cg-dna-rna.cns

#----------------------------------------------------------------------------------------------------------------#
# Copy new files
#----------------------------------------------------------------------------------------------------------------#

echo "> Copying DNA CG files"
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

echo "> Editting run.cns"
sed -i 's/{===>} cg_A=false;/{===>} cg_A=true;/g' run.cns
sed -i 's/{===>} cg_B=false;/{===>} cg_B=true;/g' run.cns
sed -i 's/{===>} cg_C=false;/{===>} cg_C=true;/g' run.cns
sed -i 's/{===>} cg_D=false;/{===>} cg_D=true;/g' run.cns
sed -i 's/{===>} cg_E=false;/{===>} cg_E=true;/g' run.cns
sed -i 's/{===>} cg_F=false;/{===>} cg_F=true;/g' run.cns

sed -i "s/{===>} dna_$DNA_CHAIN=false;/{===>} dna_$DNA_CHAIN=true;/g" run.cns

sed -i 's/{===>} solvshell=true;/{===>} solvshell=false;/g' run.cns

# set AA parameters
sed -i "s/{===>} prot_top_$DNA_CHAIN=\"protein-allhdg5-4.top\";/{===>} prot_top_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.top\";/g" run.cns
sed -i "s/{===>} prot_link_$DNA_CHAIN=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_$DNA_CHAIN=\"dna-rna-1.3.link\";/g" run.cns
sed -i "s/{===>} prot_par_$DNA_CHAIN=\"protein-allhdg5-4.param\";/{===>} prot_par_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.param\";/g" run.cns

# set CG parameters
sed -i "s/{===>} prot_cg_top_$DNA_CHAIN=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_$DNA_CHAIN=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_$DNA_CHAIN=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.param\";/g" run.cns


#----------------------------------------------------------------------------------------------------------------#
# Edit input generator
#----------------------------------------------------------------------------------------------------------------#

echo "> Editing input generator"

sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna-rna.cns' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/patch-breaks-cg-dna-rna.cns' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/dna-rna-CG-MARTINI-2-1p-break.top";' protocols/generate_$DNA_CHAIN-cg.inp
sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_$DNA_CHAIN-cg.inp

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/dna-rna-CG-MARTINI-2-1p.top/g' protocols/generate_$DNA_CHAIN-cg.inp
sed -i 's/dna-rna-1.3.link/dna-rna-CG-MARTINI-2-1p.link/g' protocols/generate_$DNA_CHAIN-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/dna-rna-CG-MARTINI-2-1p.param/g' protocols/generate_$DNA_CHAIN-cg.inp

# keep the input generator from trying to setup dihedral restraints in CG
## 
sed -i 's/dna-rna_restraints.def/dna-rna-cg_restraints.def/g' protocols/generate_$DNA_CHAIN-cg.inp

#----------------------------------------------------------------------------------------------------------------#
# Write DNA-AA restraints
#----------------------------------------------------------------------------------------------------------------#

echo "> Writing DNA-CG/AA restraints"

sed -i '/evaluate (&Data.dnarest = &dnarest_on)/a evaluate (&Data.dnacgrest = &dnacgrest_on)' run.cns

if [ -f ../dna_restraints.def ]; then
    # file exists
    sed -i '/{===>} dnarest_on=false;/a {===>} dnacgrest_on=true;' run.cns
	sed -i "s/{===>} dnarest_on=false;/{===>} dnarest_on=true;/g" run.cns

	#====#
	#
	# The files dna-aa_groups.dat and dna_restraints.def are generated by the aa2cg-prot_dna.py script!
	#
	# template-dna-rna-aa-restraints.def and dna-cg_restraints-ori.def are edited versions of the files generated by default
	#  by HADDOCK, these two files are ready for the following edits. It will not work with any other file!
	#
	#====#

	# add restraints to line 308 of template-dna-rna-aa-restraints.def
	sed "308r ../dna_restraints.def" $PARAM_FOLDER/template-dna-rna-aa-restraints.def > data/sequence/dna-rna_restraints.def

	# get groups
	AAGROUP_1=$(sed -n '1p' ../dna-aa_groups.dat)
	SEGID_1=$(sed -n '2p' ../dna-aa_groups.dat) 
	AAGROUP_2=$(sed -n '3p' ../dna-aa_groups.dat)
	SEGID_2=$(sed -n '4p' ../dna-aa_groups.dat) 

	sed -i "s/{===>} bases_planar=((resid 1:20 or resid 21:40) and segid B);/{===>} bases_planar=((resid $AAGROUP_1 or resid $AAGROUP_2) and segid $DNA_CHAIN);/g" data/sequence/dna-rna_restraints.def

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

	# add restraints to line 18 of template-dna-rna-aa-restraints.def
	sed "18r ../dna_restraints.def" $PARAM_FOLDER/template-dna-rna-cg-restraints.def > data/sequence/dna-rna-cg_restraints.def
else
	# file does not exist
	sed -i '/{===>} dnarest_on=false;/a {===>} dnacgrest_on=false;' run.cns
	# sed -i "s/{===>} dnarest_on=false;/{===>} dnarest_on=true;/g" run.cns

fi

#----------------------------------------------------------------------------------------------------------------#
# Edit refine input
#----------------------------------------------------------------------------------------------------------------#

echo "> Editing refine input"

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
##  @RUN:data/sequence/template-dna-rna-cg_restraints.def
##else
##  if ($Data.dnarest eq true ) then
##    @RUN:data/sequence/dna-rna_restraints.def
##  end if
##end if
#
sed -i "1360i if (\$Data.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-rna-cg_restraints.def\nelse\n\ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ end if\nend if" protocols/refine.inp 

# Same, but for other part of the code
sed -i '1784,1786d' protocols/refine.inp
# identation is different
sed -i "1784i \ \ if (\$Data.dnacgrest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna-cg_restraints.def\n\ \ else\n\ \ \ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ \ \ end if\n\ \ end if" protocols/refine.inp 


#----------------------------------------------------------------------------------------------------------------#
echo "> ready"
cd ..

