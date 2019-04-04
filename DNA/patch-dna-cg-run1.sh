#!/bin/bash
#============================================================================================#

#----------------------------------------------------------------------------------------------------------------#
# INPUT
#----------------------------------------------------------------------------------------------------------------#

DNA_ID=$1

# Add CG topology, parameters, link and patches
PARAM_FOLDER=/home/rodrigo/cg-params/

CG_TOP=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.top
CG_PARAM=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.param
CG_LINK=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p.link
CG_DNA_BREAK_TOP=$PARAM_FOLDER/dna-rna-CG-MARTINI-2-1p-break.top

CG_HBONDS=$PARAM_FOLDER/patch-types-cg-hbond-dna-rna.cns
CG_DNA_BREAKS=$PARAM_FOLDER/patch-breaks-cg-dna-rna.cns


#----------------------------------------------------------------------------------------------------------------#
# SET UP CG RUN
#----------------------------------------------------------------------------------------------------------------#
echo "> Setting CG run"

echo "RUN1"
cd run1

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

## this also changed to dna_molN
sed -i "s/{===>} dna_mol$DNA_ID=false;/{===>} dna_mol$DNA_ID=true;/g" run.cns

# set AA parameters
sed -i "s/{===>} prot_top_mol$DNA_ID=\"protein-allhdg5-4.top\";/{===>} prot_top_mol$DNA_ID=\"dna-rna-allatom-hj-opls-1.3.top\";/g" run.cns
sed -i "s/{===>} prot_link_mol$DNA_ID=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_mol$DNA_ID=\"dna-rna-1.3.link\";/g" run.cns
sed -i "s/{===>} prot_par_mol$DNA_ID=\"protein-allhdg5-4.param\";/{===>} prot_par_mol$DNA_ID=\"dna-rna-allatom-hj-opls-1.3.param\";/g" run.cns

# set CG parameters
sed -i "s/{===>} prot_cg_top_mol$DNA_ID=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_mol$DNA_ID=\"dna-rna-CG-MARTINI-2-1p.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_mol$DNA_ID=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_mol$DNA_ID=\"dna-rna-CG-MARTINI-2-1p.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_mol$DNA_ID=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_mol$DNA_ID=\"dna-rna-CG-MARTINI-2-1p.param\";/g" run.cns

sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

sed -i 's/{===>} epsilon_0=10.0/{===>} epsilon_0=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=1.0/{===>} epsilon_1=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=10.0/{===>} epsilon_1=78.0/g' run.cns

sed -i 's/{===>} dielec_0=rdie/{===>} dielec_0=cdie/g' run.cns
sed -i 's/{===>} dielec_1=rdie/{===>} dielec_1=rdie/g' run.cns
#----------------------------------------------------------------------------------------------------------------#
# Edit input generator
#----------------------------------------------------------------------------------------------------------------#

echo "> Editing input generator"

sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna-rna.cns' protocols/generate-cg.inp
sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/patch-breaks-cg-dna-rna.cns' protocols/generate-cg.inp
sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate-cg.inp
sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/dna-rna-CG-MARTINI-2-1p-break.top";' protocols/generate-cg.inp
sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate-cg.inp

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/dna-rna-CG-MARTINI-2-1p.top/g' protocols/generate-cg.inp
sed -i 's/dna-rna-1.3.link/dna-rna-CG-MARTINI-2-1p.link/g' protocols/generate-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/dna-rna-CG-MARTINI-2-1p.param/g' protocols/generate-cg.inp

# keep the input generator from trying to setup dihedral restraints in CG
sed -i 's/dna-rna_restraints.def/dna-rna-cg_restraints.def/g' protocols/generate-cg.inp

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

	sed -i "s/{===>} bases_planar=((resid 1:20 or resid 21:40) and segid B);/{===>} bases_planar=((resid $AAGROUP_1 or resid $AAGROUP_2) and segid $SEGID_2);/g" data/sequence/dna-rna_restraints.def

	sed -i "s/{===>} pucker_1=(resid 1:20 and segid B);/{===>} pucker_1=(resid $AAGROUP_1 and segid $SEGID_1);/g" data/sequence/dna-rna_restraints.def
	sed -i "s/{===>} pucker_2=(resid 21:40 and segid B);/{===>} pucker_2=(resid $AAGROUP_2 and segid $SEGID_2);/g" data/sequence/dna-rna_restraints.def

	sed -i "s/{===>} dihedral_1=(resid 1:20 and segid B);/{===>} dihedral_1=(resid $AAGROUP_1 and segid $SEGID_1);/g" data/sequence/dna-rna_restraints.def
	sed -i "s/{===>} dihedral_2=(resid 21:40 and segid B);/{===>} dihedral_2=(resid $AAGROUP_2 and segid $SEGID_2);/g" data/sequence/dna-rna_restraints.def

	sed -i 's/{===>} basepair_planar=false;/{===>} basepair_planar=true;/g' data/sequence/dna-rna_restraints.def

	#----------------------------------------------------------------------------------------------------------------#
	# Write DNA-CG restraints
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

#sed -i '1360,1362d' protocols/refine.inp
sed -i '1248,1250d' protocols/refine.inp

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
#sed -i "1360i if (\$Data.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-rna-cg_restraints.def\nelse\n\ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ end if\nend if" protocols/refine.inp
sed -i "1248i if (\$Data.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-rna-cg_restraints.def\nelse\n\ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ end if\nend if" protocols/refine.inp
#
## Same, but for other part of the code
##sed -i '1784,1786d' protocols/refine.inp
sed -i '1694,1696d' protocols/refine.inp
#
## identation is different
##sed -i "1784i \ \ if (\$Data.dnacgrest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna-cg_restraints.def\n\ \ else\n\ \ \ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ \ \ end if\n\ \ end if" protocols/refine.inp
sed -i "1694i \ \ if (\$Data.dnacgrest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna-cg_restraints.def\n\ \ else\n\ \ \ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ \ \ end if\n\ \ end if" protocols/refine.inp
#

#----------------------------------------------------------------------------------------------------------------#
echo "> ready"
cd ..

