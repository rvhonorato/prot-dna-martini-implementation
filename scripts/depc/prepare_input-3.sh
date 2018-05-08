#!/bin/bash

COMPLEX=$1
RECEPTOR_CHAIN=$2
LIGAND_CHAIN=$3
U_PDB_A=$4
U_PDB_B=$5

# add chains
echo ""
echo ">> Adding chains and segids:"
echo ">>> A: $U_PDB_A" 
echo ">>> B: $U_PDB_B"

sed -i .bak "s/./A/22" $U_PDB_A
sed -i .bak "s/./B/22" $U_PDB_B

# add segids
sed -i .bak "s/./A/76" $U_PDB_A
sed -i .bak "s/./B/76" $U_PDB_B

# Extract true interface from BOUND complex
echo ""
echo ">> Extracting true interface from $COMPLEX"
python ~/Nostromo/scripts/extract_interface.py $COMPLEX $RECEPTOR_CHAIN $LIGAND_CHAIN

AMBIG=${COMPLEX%.*}.tbl
cp $AMBIG ambig.tbl

# Convert unbound to CG
echo ""
echo ">> Converting to CG"
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $U_PDB_A
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $U_PDB_B # this will generate cg_restraints.def


echo ""
echo ">> Retrieving AA2CG mapping"
cat ${U_PDB_A%.*}_cg_to_aa.tbl ${U_PDB_B%.*}_cg_to_aa.tbl > aa2cg.tbl

U_PDB_A_CG=${U_PDB_A%.*}_cg.pdb
U_PDB_B_CG=${U_PDB_B%.*}_cg.pdb

echo ""
echo ">> Adding chains and segids to CG structures:"
echo ">>> A: $U_PDB_A_CG" 
echo ">>> B: $U_PDB_B_CG"
sed -i .bak "s/./A/22" $U_PDB_A_CG
sed -i .bak "s/./B/22" $U_PDB_B_CG
sed -i .bak "s/./A/76" $U_PDB_A_CG
sed -i .bak "s/./B/76" $U_PDB_B_CG

echo ""
echo ">> Saving input for HADDOCK"
echo ">>> protA: $U_PDB_A" 
echo ">>> protB: $U_PDB_B" 
echo ">>> protA_CG: $U_PDB_A_CG" 
echo ">>> protB_CG: $U_PDB_B_CG" 
echo ">>> restraints: ambig.tbl"
echo ">>> CG mapping: aa2cg.tbl"
echo ">>> DNA CG restraints: cg_restraints.def"
echo ">>> DNA AA groups: dna-aa_groups.dat"
echo ""

mkdir input
cp $U_PDB_A $U_PDB_B $U_PDB_A_CG $U_PDB_B_CG ambig.tbl aa2cg.tbl cg_restraints.def dna-aa_groups.dat input/

echo "~/run-cg.sh $U_PDB_A $U_PDB_B" > input/prepare.sh









